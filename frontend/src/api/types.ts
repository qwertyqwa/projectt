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

