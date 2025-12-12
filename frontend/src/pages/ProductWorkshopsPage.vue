<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { calculate_raw_material, fetch_product } from "../api/http";
import type { ProductDetail } from "../api/types";
import { show_alert } from "../lib/dialog";

const route = useRoute();
const router = useRouter();

const product = ref<ProductDetail | null>(null);
const loading = ref(false);

const product_id = computed(() => {
  const raw = route.params.id;
  if (typeof raw !== "string") {
    return null;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
});

const calc = reactive({
  product_quantity: "",
  parameter_one: "",
  parameter_two: "",
});

const calc_errors = reactive({
  product_quantity: "",
  parameter_one: "",
  parameter_two: "",
});

const calc_loading = ref(false);
const calc_result = ref<number | null>(null);

function normalize_number(raw: string) {
  return raw.trim().replace(",", ".");
}

function clear_calc_errors() {
  calc_errors.product_quantity = "";
  calc_errors.parameter_one = "";
  calc_errors.parameter_two = "";
}

function validate_calc() {
  clear_calc_errors();

  const quantity_text = calc.product_quantity.trim();
  if (quantity_text.length === 0) {
    calc_errors.product_quantity = "Укажите количество.";
  } else if (!/^\d+$/.test(quantity_text)) {
    calc_errors.product_quantity = "Количество должно быть целым числом.";
  } else if (Number(quantity_text) <= 0) {
    calc_errors.product_quantity = "Количество должно быть больше нуля.";
  }

  const param_one = normalize_number(calc.parameter_one);
  if (param_one.length === 0) {
    calc_errors.parameter_one = "Укажите параметр 1.";
  } else if (!/^\d+(\.\d+)?$/.test(param_one) || Number(param_one) <= 0) {
    calc_errors.parameter_one = "Параметр должен быть положительным числом.";
  }

  const param_two = normalize_number(calc.parameter_two);
  if (param_two.length === 0) {
    calc_errors.parameter_two = "Укажите параметр 2.";
  } else if (!/^\d+(\.\d+)?$/.test(param_two) || Number(param_two) <= 0) {
    calc_errors.parameter_two = "Параметр должен быть положительным числом.";
  }

  const has_errors =
    Boolean(calc_errors.product_quantity) ||
    Boolean(calc_errors.parameter_one) ||
    Boolean(calc_errors.parameter_two);

  if (has_errors) {
    show_alert(
      "warning",
      "Проверьте данные",
      "Исправьте поля, отмеченные ошибкой, и повторите расчет."
    );
  }

  return !has_errors;
}

async function load_product() {
  if (!product_id.value) {
    show_alert("error", "Ошибка", "Некорректный идентификатор продукции.");
    router.push("/products");
    return;
  }

  loading.value = true;
  try {
    product.value = await fetch_product(product_id.value);
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

function go_back() {
  if (window.history.length > 1) {
    router.back();
    return;
  }
  router.push("/products");
}

async function run_calc() {
  if (!product.value) {
    return;
  }
  if (!validate_calc()) {
    return;
  }

  calc_loading.value = true;
  try {
    const response = await calculate_raw_material({
      product_type_id: product.value.product_type_id,
      material_type_id: product.value.material_type_id,
      product_quantity: Number(calc.product_quantity),
      parameter_one: Number(normalize_number(calc.parameter_one)),
      parameter_two: Number(normalize_number(calc.parameter_two)),
    });

    calc_result.value = response.raw_material_amount;
    if (calc_result.value === -1) {
      show_alert(
        "error",
        "Ошибка",
        "Сервер вернул -1: проверьте тип продукции, материал и введенные параметры."
      );
    }
  } catch (error) {
    show_alert(
      "error",
      "Ошибка",
      error instanceof Error ? error.message : "Не удалось выполнить расчет."
    );
  } finally {
    calc_loading.value = false;
  }
}

onMounted(() => {
  load_product();
});
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Цеха для производства</h1>
      <div class="row">
        <RouterLink v-if="product_id" class="btn btn-secondary" :to="`/products/${product_id}`">
          К продукту
        </RouterLink>
        <button class="btn btn-secondary" type="button" @click="go_back">Назад</button>
      </div>
    </div>

    <div v-if="loading" class="card state">Загрузка данных...</div>

    <div v-else-if="!product" class="card state">
      Продукция не найдена или недоступна.
    </div>

    <div v-else class="stack">
      <section class="card info">
        <div class="info-title">{{ product.product_type }} | {{ product.name }}</div>
        <div class="info-meta">
          Время изготовления: <strong>{{ product.manufacture_time_hours }} ч</strong>
        </div>
      </section>

      <section class="card table-card">
        <div class="table-title">Список цехов</div>
        <table class="table">
          <thead>
            <tr>
              <th>Название цеха</th>
              <th>Количество человек</th>
              <th>Время, ч</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in product.workshops" :key="row.workshop">
              <td>{{ row.workshop }}</td>
              <td>{{ row.workers_count ?? "—" }}</td>
              <td>{{ row.manufacture_hours ?? "—" }}</td>
            </tr>
            <tr v-if="product.workshops.length === 0">
              <td colspan="3">Для продукции не задан технологический маршрут.</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="card calc">
        <div class="table-title">Расчет количества сырья</div>
        <p class="calc-text">
          Метод рассчитывает целое количество сырья с учетом потерь. Если данные
          некорректны, сервер вернет <strong>-1</strong>.
        </p>

        <div class="calc-grid">
          <div class="field">
            <label class="label" for="qty">Количество продукции</label>
            <input
              id="qty"
              v-model="calc.product_quantity"
              class="input"
              type="text"
              inputmode="numeric"
              placeholder="Например: 10"
            />
            <div v-if="calc_errors.product_quantity" class="error-text">
              {{ calc_errors.product_quantity }}
            </div>
          </div>

          <div class="field">
            <label class="label" for="p1">Параметр 1</label>
            <input
              id="p1"
              v-model="calc.parameter_one"
              class="input"
              type="text"
              inputmode="decimal"
              placeholder="Например: 1.2"
            />
            <div v-if="calc_errors.parameter_one" class="error-text">
              {{ calc_errors.parameter_one }}
            </div>
          </div>

          <div class="field">
            <label class="label" for="p2">Параметр 2</label>
            <input
              id="p2"
              v-model="calc.parameter_two"
              class="input"
              type="text"
              inputmode="decimal"
              placeholder="Например: 3.4"
            />
            <div v-if="calc_errors.parameter_two" class="error-text">
              {{ calc_errors.parameter_two }}
            </div>
          </div>
        </div>

        <div class="row calc-actions">
          <button class="btn btn-primary" type="button" :disabled="calc_loading" @click="run_calc">
            {{ calc_loading ? "Расчет..." : "Рассчитать" }}
          </button>
          <div v-if="calc_result !== null" class="calc-result">
            Необходимо сырья: <strong>{{ calc_result }}</strong>
          </div>
        </div>
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

.info {
  padding: 16px;
}

.info-title {
  font-weight: 900;
  font-size: 16px;
  margin-bottom: 8px;
}

.info-meta {
  color: var(--color-muted);
}

.table-card {
  padding: 16px;
}

.table-title {
  font-weight: 900;
  margin-bottom: 10px;
}

.calc {
  padding: 16px;
}

.calc-text {
  margin: 0 0 12px;
  color: var(--color-muted);
  line-height: 1.35;
}

.calc-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.calc-actions {
  align-items: center;
  margin-top: 14px;
}

.calc-result {
  font-weight: 900;
  color: var(--color-accent);
}

@media (max-width: 820px) {
  .calc-grid {
    grid-template-columns: 1fr;
  }
}
</style>

