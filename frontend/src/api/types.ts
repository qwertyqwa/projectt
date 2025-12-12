export type LookupItem = {
  id: number;
  name: string;
};

export type ProductListItem = {
  id: number;
  name: string;
  article: string | null;
  min_partner_price: number | null;
  product_type: string;
  product_type_id: number;
  material_type: string;
  material_type_id: number;
  manufacture_time_hours: number;
};

export type WorkshopTime = {
  workshop: string;
  workers_count: number | null;
  manufacture_hours: number | null;
};

export type ProductDetail = ProductListItem & {
  workshops: WorkshopTime[];
};

export type ProductWritePayload = {
  article: string;
  name: string;
  min_partner_price: string;
  product_type_id: number;
  material_type_id: number;
};

export type Partner = {
  id: number;
  partner_type: string;
  company_name: string;
  legal_address: string;
  inn: string;
  director_name: string;
  phone: string;
  email: string;
  logo_url: string;
  rating: number;
  sales_places: string;
};

export type PartnerWritePayload = Omit<Partner, "id">;

export type Supplier = {
  id: number;
  supplier_type: string;
  name: string;
  inn: string;
  phone: string;
  email: string;
};

export type SupplierWritePayload = Omit<Supplier, "id">;

export type Material = {
  id: number;
  name: string;
  material_type_id: number;
  material_type: string;
  supplier: number;
  supplier_name: string;
  unit: string;
  quantity_in_package: number | null;
  description: string;
  image_url: string;
  cost: string;
  stock_quantity: number;
  min_quantity: number;
};

export type MaterialWritePayload = Omit<
  Material,
  "id" | "material_type" | "supplier_name"
>;

export type Employee = {
  id: number;
  full_name: string;
  birth_date: string | null;
  passport_data: string;
  bank_details: string;
  has_family: boolean;
  health_status: string;
};

export type EmployeeWritePayload = Omit<Employee, "id">;

export type Workshop = {
  id: number;
  name: string;
  workshop_type: string | null;
  workers_count: number | null;
};

export type WorkshopWritePayload = Omit<Workshop, "id">;

export type RawMaterialCalcPayload = {
  product_type_id: number;
  material_type_id: number;
  product_quantity: number;
  parameter_one: number;
  parameter_two: number;
};

export type RawMaterialCalcResponse = {
  raw_material_amount: number;
};
