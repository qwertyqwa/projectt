import type {
  LookupItem,
  Material,
  MaterialWritePayload,
  Partner,
  PartnerWritePayload,
  ProductDetail,
  ProductListItem,
  RawMaterialCalcPayload,
  RawMaterialCalcResponse,
  ProductWritePayload,
  Supplier,
  SupplierWritePayload,
  Employee,
  EmployeeWritePayload,
  Workshop,
  WorkshopWritePayload,
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

async function request_void(path: string, init?: RequestInit): Promise<void> {
  let response: Response;
  try {
    response = await fetch(path, init);
  } catch {
    throw new Error(
      "Не удалось выполнить запрос к серверу. Проверьте, что бэкенд запущен."
    );
  }

  if (!response.ok) {
    const content_type = response.headers.get("content-type") ?? "";
    const is_json = content_type.includes("application/json");
    const body = is_json ? ((await response.json()) as ApiErrorBody) : null;
    throw new Error(build_error_message(response.status, body));
  }
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
  return request_json<Record<string, unknown>>("/api/products", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_product(id: number, payload: ProductWritePayload) {
  return request_json<Record<string, unknown>>(`/api/products/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function delete_product(id: number) {
  return request_void(`/api/products/${id}`, { method: "DELETE" });
}

export function calculate_raw_material(payload: RawMaterialCalcPayload) {
  return request_json<RawMaterialCalcResponse>("/api/raw-material/calculate", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function fetch_partners() {
  return request_json<Partner[]>("/api/partners");
}

export function fetch_partner(id: number) {
  return request_json<Partner>(`/api/partners/${id}`);
}

export function create_partner(payload: PartnerWritePayload) {
  return request_json<Partner>("/api/partners", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_partner(id: number, payload: PartnerWritePayload) {
  return request_json<Partner>(`/api/partners/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function delete_partner(id: number) {
  return request_void(`/api/partners/${id}`, { method: "DELETE" });
}

export function fetch_suppliers() {
  return request_json<Supplier[]>("/api/suppliers");
}

export function fetch_supplier(id: number) {
  return request_json<Supplier>(`/api/suppliers/${id}`);
}

export function create_supplier(payload: SupplierWritePayload) {
  return request_json<Supplier>("/api/suppliers", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_supplier(id: number, payload: SupplierWritePayload) {
  return request_json<Supplier>(`/api/suppliers/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function delete_supplier(id: number) {
  return request_void(`/api/suppliers/${id}`, { method: "DELETE" });
}

export function fetch_materials() {
  return request_json<Material[]>("/api/materials");
}

export function fetch_material(id: number) {
  return request_json<Material>(`/api/materials/${id}`);
}

export function create_material(payload: MaterialWritePayload) {
  return request_json<Material>("/api/materials", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_material(id: number, payload: MaterialWritePayload) {
  return request_json<Material>(`/api/materials/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function delete_material(id: number) {
  return request_void(`/api/materials/${id}`, { method: "DELETE" });
}

export function fetch_employees() {
  return request_json<Employee[]>("/api/employees");
}

export function fetch_employee(id: number) {
  return request_json<Employee>(`/api/employees/${id}`);
}

export function create_employee(payload: EmployeeWritePayload) {
  return request_json<Employee>("/api/employees", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_employee(id: number, payload: EmployeeWritePayload) {
  return request_json<Employee>(`/api/employees/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function delete_employee(id: number) {
  return request_void(`/api/employees/${id}`, { method: "DELETE" });
}

export function fetch_workshops() {
  return request_json<Workshop[]>("/api/workshops");
}

export function fetch_workshop(id: number) {
  return request_json<Workshop>(`/api/workshops/${id}`);
}

export function create_workshop(payload: WorkshopWritePayload) {
  return request_json<Workshop>("/api/workshops", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function update_workshop(id: number, payload: WorkshopWritePayload) {
  return request_json<Workshop>(`/api/workshops/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function delete_workshop(id: number) {
  return request_void(`/api/workshops/${id}`, { method: "DELETE" });
}
