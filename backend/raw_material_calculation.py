from __future__ import annotations

import math
import sqlite3
from pathlib import Path
from typing import Any


def _as_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_positive_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


def calculate_raw_material_amount(
    product_type_id: Any,
    material_type_id: Any,
    product_quantity: Any,
    parameter_one: Any,
    parameter_two: Any,
    db_path: str | Path | None = None,
) -> int:
    """
    Рассчитать количество сырья с учетом потерь.

    Вход:
      - product_type_id: идентификатор типа продукции (целое число)
      - material_type_id: идентификатор типа материала (целое число)
      - product_quantity: количество продукции (целое число)
      - parameter_one, parameter_two: параметры продукции (вещественные, положительные)
      - db_path: путь к furniture.db (по умолчанию рядом с этим файлом)

    Алгоритм:
      1) Сырье на 1 единицу = parameter_one * parameter_two * coefficient(product_type)
      2) Сырье на партию = сырье_на_1 * product_quantity
      3) Увеличение с учетом потерь материала:
         сырье_итого = сырье_на_партию * (1 + loss_percent(material_type))
      4) Результат округляется вверх до целого.

    Возврат:
      - целое количество сырья (>= 0) или -1 при некорректных данных.
    """

    product_type_id_int = _as_int(product_type_id)
    material_type_id_int = _as_int(material_type_id)
    product_quantity_int = _as_int(product_quantity)

    if product_type_id_int is None or product_type_id_int <= 0:
        return -1
    if material_type_id_int is None or material_type_id_int <= 0:
        return -1
    if product_quantity_int is None or product_quantity_int <= 0:
        return -1

    parameter_one_float = _as_positive_float(parameter_one)
    parameter_two_float = _as_positive_float(parameter_two)
    if parameter_one_float is None or parameter_two_float is None:
        return -1

    resolved_db_path = (
        Path(db_path).expanduser().resolve()
        if db_path is not None
        else Path(__file__).resolve().parent.parent / "furniture.db"
    )
    if not resolved_db_path.exists():
        return -1

    try:
        conn = sqlite3.connect(str(resolved_db_path))
    except sqlite3.Error:
        return -1

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT coefficient FROM product_type WHERE id = ?",
            (product_type_id_int,),
        )
        row = cursor.fetchone()
        if not row:
            return -1
        coefficient = row[0]
        if coefficient is None:
            return -1
        coefficient_float = float(coefficient)
        if not math.isfinite(coefficient_float) or coefficient_float <= 0:
            return -1

        cursor.execute(
            "SELECT loss_percent FROM material_type WHERE id = ?",
            (material_type_id_int,),
        )
        row = cursor.fetchone()
        if not row:
            return -1
        loss_percent = row[0]
        if loss_percent is None:
            return -1
        loss_value = float(loss_percent)
        if not math.isfinite(loss_value) or loss_value < 0:
            return -1

        # Если в БД потери хранятся как "проценты" (например 10), переводим в долю.
        loss_ratio = loss_value / 100.0 if loss_value > 1 else loss_value

        per_unit_raw = parameter_one_float * parameter_two_float * coefficient_float
        total_raw = per_unit_raw * product_quantity_int
        total_with_losses = total_raw * (1 + loss_ratio)

        if not math.isfinite(total_with_losses) or total_with_losses < 0:
            return -1

        return int(math.ceil(total_with_losses))
    except (sqlite3.Error, ValueError, OverflowError):
        return -1
    finally:
        conn.close()
