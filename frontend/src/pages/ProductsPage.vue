<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { fetch_products } from "../api/http";
import type { ProductListItem } from "../api/types";
import { show_alert } from "../lib/dialog";

const router = useRouter();

const products = ref<ProductListItem[]>([]);
const loading = ref(false);

function format_price(value: number | null) {
  if (value === null || value === undefined) {
    return "—";
  }
  return `${value.toFixed(2)} ₽`;
}

async function load_products() {
  loading.value = true;
  try {
    products.value = await fetch_products();
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось загрузить продукцию."
    );
  } finally {
    loading.value = false;
  }
}

function open_add() {
  router.push("/products/new");
}

function open_edit(id: number) {
  router.push(`/products/${id}`);
}

function open_workshops(id: number) {
  router.push(`/products/${id}/workshops`);
}

onMounted(() => {
  load_products();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Список продукции</h1>
      <button class="btn btn-primary" type="button" @click="open_add">
        Добавить
      </button>
    </div>

    <div v-if="loading" class="card products-state">
      Загрузка данных...
    </div>

    <div v-else-if="products.length === 0" class="card products-state">
      В базе данных пока нет продукции.
    </div>

    <div v-else class="stack">
      <article
        v-for="product in products"
        :key="product.id"
        class="card product-card"
        role="button"
        tabindex="0"
        @click="open_edit(product.id)"
        @keydown.enter="open_edit(product.id)"
      >
        <div class="product-left">
          <div class="product-top">
            <div class="product-title">
              {{ product.product_type }} | {{ product.name }}
            </div>
            <div class="product-actions">
              <button
                class="btn btn-secondary"
                type="button"
                @click.stop="open_workshops(product.id)"
              >
                Цеха
              </button>
              <button
                class="btn btn-secondary"
                type="button"
                @click.stop="open_edit(product.id)"
              >
                Редактировать
              </button>
            </div>
          </div>

          <div class="product-meta">
            Артикул: <strong>{{ product.article ?? "—" }}</strong>
          </div>
          <div class="product-meta">
            Минимальная стоимость для партнера:
            <strong>{{ format_price(product.min_partner_price) }}</strong>
          </div>
          <div class="product-meta">
            Основной материал: <strong>{{ product.material_type }}</strong>
          </div>
        </div>

        <div class="product-right">
          <div class="product-time-label">Время изготовления</div>
          <div class="product-time">{{ product.manufacture_time_hours }} ч</div>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.products-state {
  padding: 18px;
  font-weight: 700;
  color: var(--color-muted);
}

.product-card {
  padding: 16px;
  display: flex;
  gap: 18px;
  justify-content: space-between;
  align-items: stretch;
}

.product-left {
  min-width: 0;
  display: grid;
  gap: 6px;
}

.product-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.product-actions {
  display: flex;
  gap: 10px;
  flex: 0 0 auto;
}

.product-title {
  font-size: 16px;
  font-weight: 900;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-meta {
  color: var(--color-muted);
  font-size: 14px;
}

.product-meta strong {
  color: var(--color-text);
}

.product-right {
  width: 190px;
  flex: 0 0 auto;
  border-left: 1px solid var(--color-border);
  padding-left: 16px;
  display: grid;
  align-content: center;
  gap: 6px;
}

.product-time-label {
  color: var(--color-muted);
  font-weight: 800;
  font-size: 13px;
  text-align: right;
}

.product-time {
  font-size: 22px;
  font-weight: 900;
  text-align: right;
  color: var(--color-accent);
}
</style>
