<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { delete_partner, fetch_partners } from "../api/http";
import type { Partner } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const router = useRouter();

const partners = ref<Partner[]>([]);
const loading = ref(false);

async function load_partners() {
  loading.value = true;
  try {
    partners.value = await fetch_partners();
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось загрузить партнеров."
    );
  } finally {
    loading.value = false;
  }
}

function open_add() {
  router.push("/partners/new");
}

function open_edit(id: number) {
  router.push(`/partners/${id}`);
}

async function remove_partner(partner: Partner) {
  const confirmed = await show_confirm(
    "warning",
    "Удаление партнера",
    `Удалить партнера «${partner.company_name}»?\nДействие необратимо.`,
    "Удалить",
    "Отмена"
  );
  if (!confirmed) {
    return;
  }

  try {
    await delete_partner(partner.id);
    await load_partners();
    show_alert("info", "Информация", "Партнер удален.");
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось удалить партнера."
    );
  }
}

onMounted(() => {
  load_partners();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Партнеры</h1>
      <button class="btn btn-primary" type="button" @click="open_add">
        Добавить
      </button>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <div v-else class="card table-card">
      <table class="table">
        <thead>
          <tr>
            <th>Тип</th>
            <th>Компания</th>
            <th>ИНН</th>
            <th>Телефон</th>
            <th>Email</th>
            <th>Рейтинг</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="partner in partners" :key="partner.id">
            <td>{{ partner.partner_type }}</td>
            <td>
              <button
                class="link"
                type="button"
                @click="open_edit(partner.id)"
              >
                {{ partner.company_name }}
              </button>
            </td>
            <td>{{ partner.inn || "—" }}</td>
            <td>{{ partner.phone || "—" }}</td>
            <td>{{ partner.email || "—" }}</td>
            <td>{{ partner.rating }}</td>
            <td class="actions">
              <button class="btn btn-secondary" type="button" @click="open_edit(partner.id)">
                Редактировать
              </button>
              <button class="btn btn-danger" type="button" @click="remove_partner(partner)">
                Удалить
              </button>
            </td>
          </tr>
          <tr v-if="partners.length === 0">
            <td colspan="7">Партнеров пока нет.</td>
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

