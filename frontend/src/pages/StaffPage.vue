<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { delete_employee, fetch_employees } from "../api/http";
import type { Employee } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const router = useRouter();

const employees = ref<Employee[]>([]);
const loading = ref(false);

async function load_employees() {
  loading.value = true;
  try {
    employees.value = await fetch_employees();
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось загрузить сотрудников."
    );
  } finally {
    loading.value = false;
  }
}

function open_add() {
  router.push("/staff/new");
}

function open_edit(id: number) {
  router.push(`/staff/${id}`);
}

async function remove_employee(employee: Employee) {
  const confirmed = await show_confirm(
    "warning",
    "Удаление сотрудника",
    `Удалить сотрудника «${employee.full_name}»?\nДействие необратимо.`,
    "Удалить",
    "Отмена"
  );
  if (!confirmed) {
    return;
  }

  try {
    await delete_employee(employee.id);
    await load_employees();
    show_alert("info", "Информация", "Сотрудник удален.");
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось удалить сотрудника."
    );
  }
}

function format_date(value: string | null) {
  if (!value) {
    return "—";
  }
  return value;
}

onMounted(() => {
  load_employees();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Сотрудники</h1>
      <button class="btn btn-primary" type="button" @click="open_add">
        Добавить
      </button>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <div v-else class="card table-card">
      <table class="table">
        <thead>
          <tr>
            <th>ФИО</th>
            <th>Дата рождения</th>
            <th>Семья</th>
            <th>Состояние здоровья</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td>
              <button class="link" type="button" @click="open_edit(employee.id)">
                {{ employee.full_name }}
              </button>
            </td>
            <td>{{ format_date(employee.birth_date) }}</td>
            <td>{{ employee.has_family ? "Да" : "Нет" }}</td>
            <td>{{ employee.health_status || "—" }}</td>
            <td class="actions">
              <button class="btn btn-secondary" type="button" @click="open_edit(employee.id)">
                Редактировать
              </button>
              <button class="btn btn-danger" type="button" @click="remove_employee(employee)">
                Удалить
              </button>
            </td>
          </tr>
          <tr v-if="employees.length === 0">
            <td colspan="5">Сотрудников пока нет.</td>
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

