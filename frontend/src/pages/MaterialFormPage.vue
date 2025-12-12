<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";

import {
  create_material,
  fetch_material,
  fetch_material_types,
  fetch_suppliers,
  update_material,
} from "../api/http";
import type { LookupItem, MaterialWritePayload, Supplier } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const material_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const is_edit = computed(() => material_id.value !== null);
const loading = ref(false);
const saving = ref(false);

const material_types = ref<LookupItem[]>([]);
const suppliers = ref<Supplier[]>([]);

const form = reactive({
  name: "",
  material_type_id: null as number | null,
  supplier: null as number | null,
  unit: "шт",
  quantity_in_package: "",
  description: "",
  image_url: "",
  cost: "",
  stock_quantity: "0",
  min_quantity: "0",
});

const errors = reactive({
  name: "",
  material_type_id: "",
  supplier: "",
  cost: "",
  stock_quantity: "",
  min_quantity: "",
});

const initial_snapshot = ref("");

function snapshot() {
  return JSON.stringify(form);
}

const is_dirty = computed(() => initial_snapshot.value !== snapshot());

function clear_errors() {
  errors.name = "";
  errors.material_type_id = "";
  errors.supplier = "";
  errors.cost = "";
  errors.stock_quantity = "";
  errors.min_quantity = "";
}

function normalize_number(raw: string) {
  return raw.trim().replace(",", ".");
}

function validate() {
  clear_errors();

  if (form.name.trim().length === 0) {
    errors.name = "Укажите наименование материала.";
  }
  if (!form.material_type_id) {
    errors.material_type_id = "Выберите тип материала.";
  }
  if (!form.supplier) {
    errors.supplier = "Выберите поставщика.";
  }

  const price_text = normalize_number(form.cost);
  if (price_text.length === 0) {
    errors.cost = "Укажите стоимость.";
  } else if (!/^\d+(\.\d{1,2})?$/.test(price_text)) {
    errors.cost = "Стоимость должна быть числом с точностью до сотых.";
  } else if (Number(price_text) < 0) {
    errors.cost = "Стоимость не может быть отрицательной.";
  }

  if (!/^\d+$/.test(form.stock_quantity.trim())) {
    errors.stock_quantity = "Остаток должен быть целым неотрицательным числом.";
  }
  if (!/^\d+$/.test(form.min_quantity.trim())) {
    errors.min_quantity = "Минимум должен быть целым неотрицательным числом.";
  }

  const has_errors =
    Boolean(errors.name) ||
    Boolean(errors.material_type_id) ||
    Boolean(errors.supplier) ||
    Boolean(errors.cost) ||
    Boolean(errors.stock_quantity) ||
    Boolean(errors.min_quantity);

  if (has_errors) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите сохранение."
    );
  }

  return !has_errors;
}

function build_payload(): MaterialWritePayload {
  const cost_value = Number(normalize_number(form.cost)).toFixed(2);
  const quantity_in_package = form.quantity_in_package.trim();
  return {
    name: form.name.trim(),
    material_type_id: form.material_type_id ?? 0,
    supplier: form.supplier ?? 0,
    unit: form.unit.trim(),
    quantity_in_package: quantity_in_package.length === 0 ? null : Number(quantity_in_package),
    description: form.description.trim(),
    image_url: form.image_url.trim(),
    cost: cost_value,
    stock_quantity: Number(form.stock_quantity),
    min_quantity: Number(form.min_quantity),
  };
}

async function load_data() {
  loading.value = true;
  try {
    const [types, suppliers_response] = await Promise.all([
      fetch_material_types(),
      fetch_suppliers(),
    ]);
    material_types.value = types;
    suppliers.value = suppliers_response;

    if (is_edit.value && material_id.value) {
      const material = await fetch_material(material_id.value);
      form.name = material.name;
      form.material_type_id = material.material_type_id;
      form.supplier = material.supplier;
      form.unit = material.unit;
      form.quantity_in_package =
        material.quantity_in_package === null ? "" : String(material.quantity_in_package);
      form.description = material.description;
      form.image_url = material.image_url;
      form.cost = material.cost;
      form.stock_quantity = String(material.stock_quantity);
      form.min_quantity = String(material.min_quantity);
    }

    initial_snapshot.value = snapshot();
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось загрузить данные."
    );
  } finally {
    loading.value = false;
  }
}

async function save() {
  if (!validate()) {
    return;
  }

  saving.value = true;
  try {
    const payload = build_payload();
    if (is_edit.value && material_id.value) {
      await update_material(material_id.value, payload);
    } else {
      await create_material(payload);
    }
    initial_snapshot.value = snapshot();
    show_alert("success", "Информация", "Данные сохранены.");
    router.push("/warehouse");
  } catch (error) {
    show_alert(
      "error",
      "Ошибка сохранения",
      error instanceof Error ? error.message : "Не удалось сохранить данные."
    );
  } finally {
    saving.value = false;
  }
}

async function go_back() {
  if (is_dirty.value) {
    const confirmed = await show_confirm(
      "warning",
      "Несохраненные изменения",
      "Изменения не будут сохранены. Вернуться назад?",
      "Вернуться",
      "Остаться"
    );
    if (!confirmed) {
      return;
    }
  }
  router.push("/warehouse");
}

onBeforeRouteLeave(async () => {
  if (!is_dirty.value) {
    return true;
  }

  return show_confirm(
    "warning",
    "Несохраненные изменения",
    "Изменения не будут сохранены. Покинуть страницу?",
    "Покинуть",
    "Остаться"
  );
});

onMounted(() => {
  load_data();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">
        {{ is_edit ? "Редактирование материала" : "Добавление материала" }}
      </h1>
      <div class="row">
        <button class="btn btn-secondary" type="button" @click="go_back">Назад</button>
        <button class="btn btn-primary" type="button" :disabled="saving" @click="save">
          {{ saving ? "Сохранение..." : "Сохранить" }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <form v-else class="card form" @submit.prevent="save">
      <div class="form-grid">
        <div class="field form-wide">
          <label class="label" for="name">Наименование</label>
          <input id="name" v-model="form.name" class="input" type="text" />
          <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
        </div>

        <div class="field">
          <label class="label" for="material_type_id">Тип материала</label>
          <select id="material_type_id" v-model="form.material_type_id" class="select">
            <option :value="null">Выберите тип</option>
            <option v-for="item in material_types" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <div v-if="errors.material_type_id" class="error-text">{{ errors.material_type_id }}</div>
        </div>

        <div class="field">
          <label class="label" for="supplier">Поставщик</label>
          <select id="supplier" v-model="form.supplier" class="select">
            <option :value="null">Выберите поставщика</option>
            <option v-for="item in suppliers" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <div v-if="errors.supplier" class="error-text">{{ errors.supplier }}</div>
        </div>

        <div class="field">
          <label class="label" for="cost">Стоимость</label>
          <input id="cost" v-model="form.cost" class="input" type="text" inputmode="decimal" placeholder="0.00" />
          <div v-if="errors.cost" class="error-text">{{ errors.cost }}</div>
        </div>

        <div class="field">
          <label class="label" for="unit">Единица измерения</label>
          <input id="unit" v-model="form.unit" class="input" type="text" />
        </div>

        <div class="field">
          <label class="label" for="quantity_in_package">Количество в упаковке</label>
          <input id="quantity_in_package" v-model="form.quantity_in_package" class="input" type="text" inputmode="numeric" />
          <div class="hint">Поле опциональное.</div>
        </div>

        <div class="field">
          <label class="label" for="stock_quantity">Количество на складе</label>
          <input id="stock_quantity" v-model="form.stock_quantity" class="input" type="text" inputmode="numeric" />
          <div v-if="errors.stock_quantity" class="error-text">{{ errors.stock_quantity }}</div>
        </div>

        <div class="field">
          <label class="label" for="min_quantity">Минимально допустимое</label>
          <input id="min_quantity" v-model="form.min_quantity" class="input" type="text" inputmode="numeric" />
          <div v-if="errors.min_quantity" class="error-text">{{ errors.min_quantity }}</div>
        </div>

        <div class="field form-wide">
          <label class="label" for="image_url">Изображение (URL)</label>
          <input id="image_url" v-model="form.image_url" class="input" type="text" />
        </div>

        <div class="field form-wide">
          <label class="label" for="description">Описание</label>
          <input id="description" v-model="form.description" class="input" type="text" />
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>
.state {
  padding: 18px;
  font-weight: 700;
  color: var(--color-muted);
}

.form {
  padding: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.form-wide {
  grid-column: 1 / -1;
}
</style>

