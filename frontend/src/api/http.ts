import type {
  LookupItem,
  ProductDetail,
  ProductListItem,
  RawMaterialCalcPayload,
  RawMaterialCalcResponse,
  ProductWritePayload,
} from "./types";

type ApiErrorBody =
  | { detail?: string }
  | Record<string, string[] | string | number | null | undefined>;

function build_error_message(status: number, body: ApiErrorBody | null) {
  if (!body) {
    return `Ошибка запроса (HTTP ${status}).`;
  }

  if ("detail" in body && typeof body.detail === "string") {
    return body.detail;
  }

  const field_labels: Record<string, string> = {
    article: "Артикул",
    name: "Наименование",
    min_partner_price: "Стоимость",
    product_type_id: "Тип продукта",
    material_type_id: "Основной материал",
  };

  const parts: string[] = [];
  for (const [key, value] of Object.entries(body)) {
    if (!value) {
      continue;
    }
    const label = field_labels[key] ?? key;
    if (Array.isArray(value)) {
      parts.push(`${label}: ${value.join(", ")}`);
      continue;
    }
    parts.push(`${label}: ${String(value)}`);
  }

  if (parts.length === 0) {
    return `Ошибка запроса (HTTP ${status}).`;
  }

  return parts.join("\n");
}

async function request_json<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(path, init);
  } catch {
    throw new Error(
      "Не удалось выполнить запрос к серверу. Проверьте, что бэкенд запущен."
    );
  }

  const content_type = response.headers.get("content-type") ?? "";
  const is_json = content_type.includes("application/json");

  if (!response.ok) {
    const body = is_json ? ((await response.json()) as ApiErrorBody) : null;
    throw new Error(build_error_message(response.status, body));
  }

  if (!is_json) {
    throw new Error("Сервер вернул ответ не в формате JSON.");
  }

  return (await response.json()) as T;
}

export function fetch_products() {
  return request_json<ProductListItem[]>("/api/products");
}

export function fetch_product(id: number) {
  return request_json<ProductDetail>(`/api/products/${id}`);
}

export function fetch_product_types() {
  return request_json<LookupItem[]>("/api/product-types");
}

export function fetch_material_types() {
  return request_json<LookupItem[]>("/api/material-types");
}

export function create_product(payload: ProductWritePayload) {
  return request_json<ProductDetail>("/api/products", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_product(id: number, payload: ProductWritePayload) {
  return request_json<ProductDetail>(`/api/products/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function calculate_raw_material(payload: RawMaterialCalcPayload) {
  return request_json<RawMaterialCalcResponse>("/api/raw-material/calculate", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}
