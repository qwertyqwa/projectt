<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import {
  delete_material,
  delete_supplier,
  fetch_materials,
  fetch_suppliers,
} from "../api/http";
import type { Material, Supplier } from "../api/types";
import { show_alert, show_confirm } from "../lib/dialog";

const router = useRouter();

const suppliers = ref<Supplier[]>([]);
const materials = ref<Material[]>([]);
const loading = ref(false);

async function load_all() {
  loading.value = true;
  try {
    const [suppliers_response, materials_response] = await Promise.all([
      fetch_suppliers(),
      fetch_materials(),
    ]);
    suppliers.value = suppliers_response;
    materials.value = materials_response;
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось загрузить данные склада."
    );
  } finally {
    loading.value = false;
  }
}

function open_add_supplier() {
  router.push("/warehouse/suppliers/new");
}

function open_edit_supplier(id: number) {
  router.push(`/warehouse/suppliers/${id}`);
}

async function remove_supplier(supplier: Supplier) {
  const confirmed = await show_confirm(
    "warning",
    "Удаление поставщика",
    `Удалить поставщика «${supplier.name}»?\nЕсли поставщик используется в материалах, сервер может запретить удаление.`,
    "Удалить",
    "Отмена"
  );
  if (!confirmed) {
    return;
  }

  try {
    await delete_supplier(supplier.id);
    await load_all();
    show_alert("info", "Информация", "Поставщик удален.");
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось удалить поставщика."
    );
  }
}

function open_add_material() {
  router.push("/warehouse/materials/new");
}

function open_edit_material(id: number) {
  router.push(`/warehouse/materials/${id}`);
}

async function remove_material(material: Material) {
  const confirmed = await show_confirm(
    "warning",
    "Удаление материала",
    `Удалить материал «${material.name}»?\nДействие необратимо.`,
    "Удалить",
    "Отмена"
  );
  if (!confirmed) {
    return;
  }

  try {
    await delete_material(material.id);
    await load_all();
    show_alert("info", "Информация", "Материал удален.");
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось удалить материал."
    );
  }
}

function format_money(value: string) {
  const num = Number(value);
  if (!Number.isFinite(num)) {
    return value;
  }
  return `${num.toFixed(2)} ₽`;
}

onMounted(() => {
  load_all();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Склад и материалы</h1>
      <button class="btn btn-secondary" type="button" :disabled="loading" @click="load_all">
        Обновить
      </button>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <div v-else class="stack">
      <section class="card table-card">
        <div class="section-header">
          <div class="section-title">Поставщики</div>
          <button class="btn btn-primary" type="button" @click="open_add_supplier">
            Добавить
          </button>
        </div>

        <table class="table">
          <thead>
            <tr>
              <th>Тип</th>
              <th>Название</th>
              <th>ИНН</th>
              <th>Телефон</th>
              <th>Email</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="supplier in suppliers" :key="supplier.id">
              <td>{{ supplier.supplier_type }}</td>
              <td>
                <button class="link" type="button" @click="open_edit_supplier(supplier.id)">
                  {{ supplier.name }}
                </button>
              </td>
              <td>{{ supplier.inn || "—" }}</td>
              <td>{{ supplier.phone || "—" }}</td>
              <td>{{ supplier.email || "—" }}</td>
              <td class="actions">
                <button class="btn btn-secondary" type="button" @click="open_edit_supplier(supplier.id)">
                  Редактировать
                </button>
                <button class="btn btn-danger" type="button" @click="remove_supplier(supplier)">
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="suppliers.length === 0">
              <td colspan="6">Поставщиков пока нет.</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="card table-card">
        <div class="section-header">
          <div class="section-title">Материалы</div>
          <button class="btn btn-primary" type="button" @click="open_add_material">
            Добавить
          </button>
        </div>

        <table class="table">
          <thead>
            <tr>
              <th>Наименование</th>
              <th>Тип материала</th>
              <th>Поставщик</th>
              <th>Цена</th>
              <th>Остаток</th>
              <th>Мин.</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="material in materials" :key="material.id">
              <td>
                <button class="link" type="button" @click="open_edit_material(material.id)">
                  {{ material.name }}
                </button>
              </td>
              <td>{{ material.material_type }}</td>
              <td>{{ material.supplier_name }}</td>
              <td>{{ format_money(material.cost) }}</td>
              <td>{{ material.stock_quantity }}</td>
              <td>{{ material.min_quantity }}</td>
              <td class="actions">
                <button class="btn btn-secondary" type="button" @click="open_edit_material(material.id)">
                  Редактировать
                </button>
                <button class="btn btn-danger" type="button" @click="remove_material(material)">
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="materials.length === 0">
              <td colspan="7">Материалов пока нет.</td>
            </tr>
          </tbody>
        </table>
      </section>
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

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.section-title {
  font-weight: 900;
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

