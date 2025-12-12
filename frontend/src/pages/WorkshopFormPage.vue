<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router";

import { create_workshop, fetch_workshop, update_workshop } from "../api/http";
import type { WorkshopWritePayload } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const workshop_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const is_edit = computed(() => workshop_id.value !== null);
const loading = ref(false);
const saving = ref(false);

const form = reactive({
  name: "",
  workshop_type: "",
  workers_count: "",
});

const errors = reactive({
  name: "",
  workers_count: "",
});

const initial_snapshot = ref("");

function snapshot() {
  return JSON.stringify(form);
}

const is_dirty = computed(() => initial_snapshot.value !== snapshot());

function clear_errors() {
  errors.name = "";
  errors.workers_count = "";
}

function validate() {
  clear_errors();

  if (form.name.trim().length === 0) {
    errors.name = "Укажите название цеха.";
  }

  const workers_text = form.workers_count.trim();
  if (workers_text.length > 0) {
    if (!/^\d+$/.test(workers_text)) {
      errors.workers_count = "Количество человек должно быть целым неотрицательным числом.";
    }
  }

  const has_errors = Boolean(errors.name) || Boolean(errors.workers_count);
  if (has_errors) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите сохранение."
    );
  }

  return !has_errors;
}

function build_payload(): WorkshopWritePayload {
  const workers_text = form.workers_count.trim();
  return {
    name: form.name.trim(),
    workshop_type: form.workshop_type.trim().length === 0 ? null : form.workshop_type.trim(),
    workers_count: workers_text.length === 0 ? null : Number(workers_text),
  };
}

async function load_data() {
  loading.value = true;
  try {
    if (is_edit.value && workshop_id.value) {
      const workshop = await fetch_workshop(workshop_id.value);
      form.name = workshop.name;
      form.workshop_type = workshop.workshop_type ?? "";
      form.workers_count = workshop.workers_count === null ? "" : String(workshop.workers_count);
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
    if (is_edit.value && workshop_id.value) {
      await update_workshop(workshop_id.value, payload);
    } else {
      await create_workshop(payload);
    }
    initial_snapshot.value = snapshot();
    show_alert("success", "Информация", "Данные сохранены.");
    router.push("/production");
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
  router.push("/production");
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
        {{ is_edit ? "Редактирование цеха" : "Добавление цеха" }}
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
          <label class="label" for="name">Название</label>
          <input id="name" v-model="form.name" class="input" type="text" />
          <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
        </div>

        <div class="field">
          <label class="label" for="workshop_type">Тип</label>
          <input id="workshop_type" v-model="form.workshop_type" class="input" type="text" />
          <div class="hint">Поле опциональное.</div>
        </div>

        <div class="field">
          <label class="label" for="workers_count">Количество человек</label>
          <input
            id="workers_count"
            v-model="form.workers_count"
            class="input"
            type="text"
            inputmode="numeric"
          />
          <div class="hint">Поле опциональное. Если не указано — будет «—».</div>
          <div v-if="errors.workers_count" class="error-text">{{ errors.workers_count }}</div>
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

