<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";

import {
  create_product,
  fetch_material_types,
  fetch_product,
  fetch_product_types,
  update_product,
} from "../api/http";
import type { LookupItem, ProductWritePayload } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const product_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const is_edit = computed(() => product_id.value !== null);
const loading = ref(false);
const saving = ref(false);

const product_types = ref<LookupItem[]>([]);
const material_types = ref<LookupItem[]>([]);

const form = reactive({
  article: "",
  name: "",
  min_partner_price: "",
  product_type_id: null as number | null,
  material_type_id: null as number | null,
});

const errors = reactive({
  article: "",
  name: "",
  min_partner_price: "",
  product_type_id: "",
  material_type_id: "",
});

const initial_snapshot = ref("");

function snapshot() {
  return JSON.stringify({
    article: form.article,
    name: form.name,
    min_partner_price: form.min_partner_price,
    product_type_id: form.product_type_id,
    material_type_id: form.material_type_id,
  });
}

const is_dirty = computed(() => initial_snapshot.value !== snapshot());

function clear_errors() {
  errors.article = "";
  errors.name = "";
  errors.min_partner_price = "";
  errors.product_type_id = "";
  errors.material_type_id = "";
}

function normalize_price(raw: string) {
  return raw.trim().replace(",", ".");
}

function validate() {
  clear_errors();

  if (form.article.trim().length === 0) {
    errors.article = "Укажите артикул.";
  }
  if (form.name.trim().length === 0) {
    errors.name = "Укажите наименование продукции.";
  }
  if (!form.product_type_id) {
    errors.product_type_id = "Выберите тип продукта.";
  }
  if (!form.material_type_id) {
    errors.material_type_id = "Выберите основной материал.";
  }

  const normalized_price = normalize_price(form.min_partner_price);
  if (normalized_price.length === 0) {
    errors.min_partner_price = "Укажите стоимость.";
  } else if (!/^\d+(\.\d{1,2})?$/.test(normalized_price)) {
    errors.min_partner_price =
      "Стоимость должна быть числом с точностью до сотых (например, 1234.50).";
  } else if (Number(normalized_price) < 0) {
    errors.min_partner_price = "Стоимость не может быть отрицательной.";
  }

  const has_errors =
    Boolean(errors.article) ||
    Boolean(errors.name) ||
    Boolean(errors.min_partner_price) ||
    Boolean(errors.product_type_id) ||
    Boolean(errors.material_type_id);

  if (has_errors) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите сохранение."
    );
  }

  return !has_errors;
}

async function load_data() {
  loading.value = true;
  try {
    const [types, materials] = await Promise.all([
      fetch_product_types(),
      fetch_material_types(),
    ]);
    product_types.value = types;
    material_types.value = materials;

    if (is_edit.value && product_id.value) {
      const product = await fetch_product(product_id.value);
      form.article = product.article ?? "";
      form.name = product.name;
      form.min_partner_price =
        product.min_partner_price === null
          ? ""
          : product.min_partner_price.toFixed(2);
      form.product_type_id = product.product_type_id;
      form.material_type_id = product.material_type_id;
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

function build_payload(): ProductWritePayload {
  // Цена отправляется строкой, чтобы сохранить точность до сотых.
  const normalized_price = normalize_price(form.min_partner_price);
  const fixed_price = Number(normalized_price).toFixed(2);

  return {
    article: form.article.trim(),
    name: form.name.trim(),
    min_partner_price: fixed_price,
    product_type_id: form.product_type_id ?? 0,
    material_type_id: form.material_type_id ?? 0,
  };
}

async function save() {
  if (!validate()) {
    return;
  }

  saving.value = true;
  try {
    const payload = build_payload();
    if (is_edit.value && product_id.value) {
      await update_product(product_id.value, payload);
    } else {
      await create_product(payload);
    }
    initial_snapshot.value = snapshot();
    show_alert(
      "success",
      "Информация",
      "Данные сохранены. Список продукции будет обновлен."
    );
    router.push("/products");
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

  if (window.history.length > 1) {
    router.back();
    return;
  }
  router.push("/products");
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
        {{ is_edit ? "Редактирование продукции" : "Добавление продукции" }}
      </h1>
      <div class="row">
        <button class="btn btn-secondary" type="button" @click="go_back">
          Назад
        </button>
        <RouterLink
          v-if="is_edit && product_id"
          class="btn btn-secondary"
          :to="`/products/${product_id}/workshops`"
        >
          Цеха
        </RouterLink>
        <button class="btn btn-primary" type="button" :disabled="saving" @click="save">
          {{ saving ? "Сохранение..." : "Сохранить" }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="card form-state">Загрузка данных...</div>

    <form v-else class="card form" @submit.prevent="save">
      <div class="form-grid">
        <div class="field">
          <label class="label" for="article">Артикул</label>
          <input
            id="article"
            v-model="form.article"
            class="input"
            type="text"
            placeholder="Например: 7758953"
          />
          <div v-if="errors.article" class="error-text">{{ errors.article }}</div>
        </div>

        <div class="field">
          <label class="label" for="product_type">Тип продукта</label>
          <select
            id="product_type"
            v-model="form.product_type_id"
            class="select"
          >
            <option :value="null">Выберите тип</option>
            <option v-for="item in product_types" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <div v-if="errors.product_type_id" class="error-text">
            {{ errors.product_type_id }}
          </div>
        </div>

        <div class="field form-wide">
          <label class="label" for="name">Наименование</label>
          <input
            id="name"
            v-model="form.name"
            class="input"
            type="text"
            placeholder="Введите наименование продукции"
          />
          <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
        </div>

        <div class="field">
          <label class="label" for="price">Минимальная стоимость для партнера</label>
          <input
            id="price"
            v-model="form.min_partner_price"
            class="input"
            type="text"
            inputmode="decimal"
            placeholder="Например: 25990.00"
          />
          <div class="hint">Стоимость не может быть отрицательной.</div>
          <div v-if="errors.min_partner_price" class="error-text">
            {{ errors.min_partner_price }}
          </div>
        </div>

        <div class="field">
          <label class="label" for="material_type">Основной материал</label>
          <select
            id="material_type"
            v-model="form.material_type_id"
            class="select"
          >
            <option :value="null">Выберите материал</option>
            <option v-for="item in material_types" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <div v-if="errors.material_type_id" class="error-text">
            {{ errors.material_type_id }}
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-state {
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
