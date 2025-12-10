import sqlite3
from pathlib import Path

import pandas as pd

DB_NAME = "furniture.db"
DATA_DIR = Path(".")  # папка, где лежат файлы *_import.xlsx

FILE_PRODUCTS = DATA_DIR / "Products_import.xlsx"
FILE_PRODUCT_TYPES = DATA_DIR / "Product_type_import.xlsx"
FILE_MATERIAL_TYPES = DATA_DIR / "Material_type_import.xlsx"
FILE_WORKSHOPS = DATA_DIR / "Workshops_import.xlsx"
FILE_PRODUCT_WORKSHOPS = DATA_DIR / "Product_workshops_import.xlsx"


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON")

    cur = conn.cursor()

    # Тип продукции
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS product_type (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL UNIQUE,
            coefficient     REAL
        );
        """
    )

    # Тип материала
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS material_type (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL UNIQUE,
            loss_percent    REAL
        );
        """
    )

    # Цех
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS workshop (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            name                    TEXT NOT NULL UNIQUE,
            workshop_type           TEXT,
            workers_count           INTEGER
        );
        """
    )

    # Продукция
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS product (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            name                    TEXT NOT NULL UNIQUE,
            article                 TEXT,
            min_partner_price       REAL,
            product_type_id         INTEGER NOT NULL,
            material_type_id        INTEGER NOT NULL,
            FOREIGN KEY (product_type_id)  REFERENCES product_type(id),
            FOREIGN KEY (material_type_id) REFERENCES material_type(id)
        );
        """
    )

    # Связь продукция – цех
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS product_workshop (
            product_id          INTEGER NOT NULL,
            workshop_id         INTEGER NOT NULL,
            manufacture_hours   REAL,
            PRIMARY KEY (product_id, workshop_id),
            FOREIGN KEY (product_id)  REFERENCES product(id),
            FOREIGN KEY (workshop_id) REFERENCES workshop(id)
        );
        """
    )

    conn.commit()


def load_product_types(conn: sqlite3.Connection) -> None:
    df = pd.read_excel(FILE_PRODUCT_TYPES)
    df.columns = [c.strip() for c in df.columns]

    cur = conn.cursor()
    for _, row in df.iterrows():
        name = str(row["Тип продукции"]).strip()
        coef = float(row["Коэффициент типа продукции"])
        cur.execute(
            """
            INSERT OR IGNORE INTO product_type (name, coefficient)
            VALUES (?, ?)
            """,
            (name, coef),
        )
    conn.commit()


def load_material_types(conn: sqlite3.Connection) -> None:
    df = pd.read_excel(FILE_MATERIAL_TYPES)
    df.columns = [c.strip() for c in df.columns]

    cur = conn.cursor()
    for _, row in df.iterrows():
        name = str(row["Тип материала"]).strip()
        loss = float(row["Процент потерь сырья"])
        cur.execute(
            """
            INSERT OR IGNORE INTO material_type (name, loss_percent)
            VALUES (?, ?)
            """,
            (name, loss),
        )
    conn.commit()


def load_workshops(conn: sqlite3.Connection) -> None:
    df = pd.read_excel(FILE_WORKSHOPS)
    # убираем лишние пробелы в названиях колонок
    df.columns = [c.strip() for c in df.columns]

    cur = conn.cursor()
    for _, row in df.iterrows():
        name = str(row["Название цеха"]).strip()
        wtype = str(row["Тип цеха"]).strip() if not pd.isna(row["Тип цеха"]) else None
        workers_raw = row["Количество человек для производства"]
        workers = int(workers_raw) if not pd.isna(workers_raw) else None

        cur.execute(
            """
            INSERT OR IGNORE INTO workshop (name, workshop_type, workers_count)
            VALUES (?, ?, ?)
            """,
            (name, wtype, workers),
        )
    conn.commit()


def build_lookup(conn: sqlite3.Connection, table: str, name_column: str = "name") -> dict:
    cur = conn.cursor()
    cur.execute(f"SELECT id, {name_column} FROM {table}")
    return {row[1]: row[0] for row in cur.fetchall()}


def load_products(conn: sqlite3.Connection) -> None:
    df = pd.read_excel(FILE_PRODUCTS)
    df.columns = [c.strip() for c in df.columns]

    # словари "значение -> id" из справочников
    product_type_map = build_lookup(conn, "product_type")
    material_type_map = build_lookup(conn, "material_type")

    cur = conn.cursor()
    for _, row in df.iterrows():
        p_type_name = str(row["Тип продукции"]).strip()
        material_name = str(row["Основной материал"]).strip()

        product_type_id = product_type_map.get(p_type_name)
        material_type_id = material_type_map.get(material_name)

        if product_type_id is None:
            raise ValueError(f"Не найден тип продукции: {p_type_name}")
        if material_type_id is None:
            raise ValueError(f"Не найден тип материала: {material_name}")

        name = str(row["Наименование продукции"]).strip()
        article = str(row["Артикул"]).strip()
        min_price = float(row["Минимальная стоимость для партнера"])

        cur.execute(
            """
            INSERT OR IGNORE INTO product
                (name, article, min_partner_price, product_type_id, material_type_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, article, min_price, product_type_id, material_type_id),
        )
    conn.commit()


def load_product_workshops(conn: sqlite3.Connection) -> None:
    df = pd.read_excel(FILE_PRODUCT_WORKSHOPS)
    df.columns = [c.strip() for c in df.columns]

    product_map = build_lookup(conn, "product")
    workshop_map = build_lookup(conn, "workshop")

    cur = conn.cursor()
    for _, row in df.iterrows():
        product_name = str(row["Наименование продукции"]).strip()
        workshop_name = str(row["Название цеха"]).strip()
        hours_raw = row["Время изготовления, ч"]
        hours = float(hours_raw) if not pd.isna(hours_raw) else None

        product_id = product_map.get(product_name)
        workshop_id = workshop_map.get(workshop_name)

        if product_id is None:
            raise ValueError(f"Не найдена продукция: {product_name}")
        if workshop_id is None:
            raise ValueError(f"Не найден цех: {workshop_name}")

        cur.execute(
            """
            INSERT OR REPLACE INTO product_workshop
                (product_id, workshop_id, manufacture_hours)
            VALUES (?, ?, ?)
            """,
            (product_id, workshop_id, hours),
        )
    conn.commit()


def main():
    conn = sqlite3.connect(DB_NAME)
    try:
        create_tables(conn)
        load_product_types(conn)
        load_material_types(conn)
        load_workshops(conn)
        load_products(conn)
        load_product_workshops(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
