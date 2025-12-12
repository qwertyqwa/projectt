<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { delete_workshop, fetch_workshops } from "../api/http";
import type { Workshop } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const router = useRouter();

const workshops = ref<Workshop[]>([]);
const loading = ref(false);

async function load_workshops() {
  loading.value = true;
  try {
    workshops.value = await fetch_workshops();
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось загрузить цеха."
    );
  } finally {
    loading.value = false;
  }
}

function open_add() {
  router.push("/production/workshops/new");
}

function open_edit(id: number) {
  router.push(`/production/workshops/${id}`);
}

async function remove_workshop(workshop: Workshop) {
  const confirmed = await show_confirm(
    "warning",
    "Удаление цеха",
    `Удалить цех «${workshop.name}»?\nДействие необратимо.`,
    "Удалить",
    "Отмена"
  );
  if (!confirmed) {
    return;
  }

  try {
    await delete_workshop(workshop.id);
    await load_workshops();
    show_alert("info", "Информация", "Цех удален.");
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось удалить цех."
    );
  }
}

onMounted(() => {
  load_workshops();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Производство</h1>
      <button class="btn btn-primary" type="button" @click="open_add">
        Добавить цех
      </button>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <div v-else class="card table-card">
      <div class="section-title">Цеха</div>
      <table class="table">
        <thead>
          <tr>
            <th>Название</th>
            <th>Тип</th>
            <th>Количество человек</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="workshop in workshops" :key="workshop.id">
            <td>
              <button class="link" type="button" @click="open_edit(workshop.id)">
                {{ workshop.name }}
              </button>
            </td>
            <td>{{ workshop.workshop_type ?? "—" }}</td>
            <td>{{ workshop.workers_count ?? "—" }}</td>
            <td class="actions">
              <button class="btn btn-secondary" type="button" @click="open_edit(workshop.id)">
                Редактировать
              </button>
              <button class="btn btn-danger" type="button" @click="remove_workshop(workshop)">
                Удалить
              </button>
            </td>
          </tr>
          <tr v-if="workshops.length === 0">
            <td colspan="4">Цехов пока нет.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.state {
  padding: 18px;
  font-weight: 700;
  color: var(--color-muted);
}

.table-card {
  padding: 16px;
}

.section-title {
  font-weight: 900;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.link {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  color: var(--color-accent);
  cursor: pointer;
  font-weight: 800;
}
</style>

