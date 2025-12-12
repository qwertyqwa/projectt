<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";

import { create_partner, fetch_partner, update_partner } from "../api/http";
import type { PartnerWritePayload } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const partner_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const is_edit = computed(() => partner_id.value !== null);
const loading = ref(false);
const saving = ref(false);

const form = reactive({
  partner_type: "",
  company_name: "",
  legal_address: "",
  inn: "",
  director_name: "",
  phone: "",
  email: "",
  logo_url: "",
  rating: "0",
  sales_places: "",
});

const errors = reactive({
  partner_type: "",
  company_name: "",
  rating: "",
});

const initial_snapshot = ref("");

function snapshot() {
  return JSON.stringify(form);
}

const is_dirty = computed(() => initial_snapshot.value !== snapshot());

function clear_errors() {
  errors.partner_type = "";
  errors.company_name = "";
  errors.rating = "";
}

function validate() {
  clear_errors();

  if (form.partner_type.trim().length === 0) {
    errors.partner_type = "Укажите тип партнера.";
  }
  if (form.company_name.trim().length === 0) {
    errors.company_name = "Укажите наименование компании.";
  }

  const rating_value = Number(form.rating);
  if (!Number.isFinite(rating_value) || !Number.isInteger(rating_value)) {
    errors.rating = "Рейтинг должен быть целым числом от 0 до 10.";
  } else if (rating_value < 0 || rating_value > 10) {
    errors.rating = "Рейтинг должен быть в диапазоне 0–10.";
  }

  const has_errors =
    Boolean(errors.partner_type) ||
    Boolean(errors.company_name) ||
    Boolean(errors.rating);

  if (has_errors) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите сохранение."
    );
  }

  return !has_errors;
}

function build_payload(): PartnerWritePayload {
  return {
    partner_type: form.partner_type.trim(),
    company_name: form.company_name.trim(),
    legal_address: form.legal_address.trim(),
    inn: form.inn.trim(),
    director_name: form.director_name.trim(),
    phone: form.phone.trim(),
    email: form.email.trim(),
    logo_url: form.logo_url.trim(),
    rating: Number(form.rating),
    sales_places: form.sales_places.trim(),
  };
}

async function load_data() {
  loading.value = true;
  try {
    if (is_edit.value && partner_id.value) {
      const partner = await fetch_partner(partner_id.value);
      form.partner_type = partner.partner_type;
      form.company_name = partner.company_name;
      form.legal_address = partner.legal_address;
      form.inn = partner.inn;
      form.director_name = partner.director_name;
      form.phone = partner.phone;
      form.email = partner.email;
      form.logo_url = partner.logo_url;
      form.rating = String(partner.rating);
      form.sales_places = partner.sales_places;
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
    if (is_edit.value && partner_id.value) {
      await update_partner(partner_id.value, payload);
    } else {
      await create_partner(payload);
    }
    initial_snapshot.value = snapshot();
    show_alert("success", "Информация", "Данные сохранены.");
    router.push("/partners");
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
  router.push("/partners");
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
        {{ is_edit ? "Редактирование партнера" : "Добавление партнера" }}
      </h1>
      <div class="row">
        <button class="btn btn-secondary" type="button" @click="go_back">
          Назад
        </button>
        <button class="btn btn-primary" type="button" :disabled="saving" @click="save">
          {{ saving ? "Сохранение..." : "Сохранить" }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <form v-else class="card form" @submit.prevent="save">
      <div class="form-grid">
        <div class="field">
          <label class="label" for="partner_type">Тип</label>
          <input id="partner_type" v-model="form.partner_type" class="input" type="text" />
          <div v-if="errors.partner_type" class="error-text">{{ errors.partner_type }}</div>
        </div>

        <div class="field">
          <label class="label" for="rating">Рейтинг (0–10)</label>
          <input id="rating" v-model="form.rating" class="input" type="text" inputmode="numeric" />
          <div v-if="errors.rating" class="error-text">{{ errors.rating }}</div>
        </div>

        <div class="field form-wide">
          <label class="label" for="company_name">Наименование компании</label>
          <input id="company_name" v-model="form.company_name" class="input" type="text" />
          <div v-if="errors.company_name" class="error-text">{{ errors.company_name }}</div>
        </div>

        <div class="field form-wide">
          <label class="label" for="legal_address">Юридический адрес</label>
          <input id="legal_address" v-model="form.legal_address" class="input" type="text" />
        </div>

        <div class="field">
          <label class="label" for="inn">ИНН</label>
          <input id="inn" v-model="form.inn" class="input" type="text" inputmode="numeric" />
        </div>

        <div class="field">
          <label class="label" for="director_name">ФИО директора</label>
          <input id="director_name" v-model="form.director_name" class="input" type="text" />
        </div>

        <div class="field">
          <label class="label" for="phone">Телефон</label>
          <input id="phone" v-model="form.phone" class="input" type="text" />
        </div>

        <div class="field">
          <label class="label" for="email">Email</label>
          <input id="email" v-model="form.email" class="input" type="email" />
        </div>

        <div class="field form-wide">
          <label class="label" for="logo_url">Логотип (URL)</label>
          <input id="logo_url" v-model="form.logo_url" class="input" type="text" />
          <div class="hint">Поле опциональное. Можно указать ссылку на изображение.</div>
        </div>

        <div class="field form-wide">
          <label class="label" for="sales_places">Места продаж</label>
          <input id="sales_places" v-model="form.sales_places" class="input" type="text" />
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

