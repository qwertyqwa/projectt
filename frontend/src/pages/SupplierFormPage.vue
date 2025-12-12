<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";

import { create_supplier, fetch_supplier, update_supplier } from "../api/http";
import type { SupplierWritePayload } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const supplier_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const is_edit = computed(() => supplier_id.value !== null);
const loading = ref(false);
const saving = ref(false);

const form = reactive({
  supplier_type: "",
  name: "",
  inn: "",
  phone: "",
  email: "",
});

const errors = reactive({
  supplier_type: "",
  name: "",
});

const initial_snapshot = ref("");

function snapshot() {
  return JSON.stringify(form);
}

const is_dirty = computed(() => initial_snapshot.value !== snapshot());

function clear_errors() {
  errors.supplier_type = "";
  errors.name = "";
}

function validate() {
  clear_errors();

  if (form.supplier_type.trim().length === 0) {
    errors.supplier_type = "Укажите тип поставщика.";
  }
  if (form.name.trim().length === 0) {
    errors.name = "Укажите название поставщика.";
  }

  const has_errors = Boolean(errors.supplier_type) || Boolean(errors.name);
  if (has_errors) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите сохранение."
    );
  }

  return !has_errors;
}

function build_payload(): SupplierWritePayload {
  return {
    supplier_type: form.supplier_type.trim(),
    name: form.name.trim(),
    inn: form.inn.trim(),
    phone: form.phone.trim(),
    email: form.email.trim(),
  };
}

async function load_data() {
  loading.value = true;
  try {
    if (is_edit.value && supplier_id.value) {
      const supplier = await fetch_supplier(supplier_id.value);
      form.supplier_type = supplier.supplier_type;
      form.name = supplier.name;
      form.inn = supplier.inn;
      form.phone = supplier.phone;
      form.email = supplier.email;
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
    if (is_edit.value && supplier_id.value) {
      await update_supplier(supplier_id.value, payload);
    } else {
      await create_supplier(payload);
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
        {{ is_edit ? "Редактирование поставщика" : "Добавление поставщика" }}
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
        <div class="field">
          <label class="label" for="supplier_type">Тип</label>
          <input id="supplier_type" v-model="form.supplier_type" class="input" type="text" />
          <div v-if="errors.supplier_type" class="error-text">{{ errors.supplier_type }}</div>
        </div>

        <div class="field">
          <label class="label" for="name">Название</label>
          <input id="name" v-model="form.name" class="input" type="text" />
          <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
        </div>

        <div class="field">
          <label class="label" for="inn">ИНН</label>
          <input id="inn" v-model="form.inn" class="input" type="text" inputmode="numeric" />
        </div>

        <div class="field">
          <label class="label" for="phone">Телефон</label>
          <input id="phone" v-model="form.phone" class="input" type="text" />
        </div>

        <div class="field form-wide">
          <label class="label" for="email">Email</label>
          <input id="email" v-model="form.email" class="input" type="email" />
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

