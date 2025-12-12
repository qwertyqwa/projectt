<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";

import { create_employee, fetch_employee, update_employee } from "../api/http";
import type { EmployeeWritePayload } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const employee_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const is_edit = computed(() => employee_id.value !== null);
const loading = ref(false);
const saving = ref(false);

const form = reactive({
  full_name: "",
  birth_date: "",
  passport_data: "",
  bank_details: "",
  has_family: false,
  health_status: "",
});

const errors = reactive({
  full_name: "",
});

const initial_snapshot = ref("");

function snapshot() {
  return JSON.stringify(form);
}

const is_dirty = computed(() => initial_snapshot.value !== snapshot());

function clear_errors() {
  errors.full_name = "";
}

function validate() {
  clear_errors();

  if (form.full_name.trim().length < 3) {
    errors.full_name = "Укажите ФИО (минимум 3 символа).";
  }

  if (errors.full_name) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите сохранение."
    );
  }

  return !errors.full_name;
}

function build_payload(): EmployeeWritePayload {
  return {
    full_name: form.full_name.trim(),
    birth_date: form.birth_date.trim().length === 0 ? null : form.birth_date.trim(),
    passport_data: form.passport_data.trim(),
    bank_details: form.bank_details.trim(),
    has_family: form.has_family,
    health_status: form.health_status.trim(),
  };
}

async function load_data() {
  loading.value = true;
  try {
    if (is_edit.value && employee_id.value) {
      const employee = await fetch_employee(employee_id.value);
      form.full_name = employee.full_name;
      form.birth_date = employee.birth_date ?? "";
      form.passport_data = employee.passport_data;
      form.bank_details = employee.bank_details;
      form.has_family = employee.has_family;
      form.health_status = employee.health_status;
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
    if (is_edit.value && employee_id.value) {
      await update_employee(employee_id.value, payload);
    } else {
      await create_employee(payload);
    }
    initial_snapshot.value = snapshot();
    show_alert("success", "Информация", "Данные сохранены.");
    router.push("/staff");
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
  router.push("/staff");
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
        {{ is_edit ? "Редактирование сотрудника" : "Добавление сотрудника" }}
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
        <div class="field form-wide">
          <label class="label" for="full_name">ФИО</label>
          <input id="full_name" v-model="form.full_name" class="input" type="text" />
          <div v-if="errors.full_name" class="error-text">{{ errors.full_name }}</div>
        </div>

        <div class="field">
          <label class="label" for="birth_date">Дата рождения</label>
          <input id="birth_date" v-model="form.birth_date" class="input" type="date" />
        </div>

        <div class="field">
          <label class="label" for="has_family">Наличие семьи</label>
          <select id="has_family" v-model="form.has_family" class="select">
            <option :value="false">Нет</option>
            <option :value="true">Да</option>
          </select>
        </div>

        <div class="field form-wide">
          <label class="label" for="passport">Паспортные данные</label>
          <input id="passport" v-model="form.passport_data" class="input" type="text" />
        </div>

        <div class="field form-wide">
          <label class="label" for="bank">Банковские реквизиты</label>
          <input id="bank" v-model="form.bank_details" class="input" type="text" />
        </div>

        <div class="field form-wide">
          <label class="label" for="health">Состояние здоровья</label>
          <input id="health" v-model="form.health_status" class="input" type="text" />
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

