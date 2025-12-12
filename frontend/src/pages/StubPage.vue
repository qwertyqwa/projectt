<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
const title = (route.meta.title as string | undefined) ?? "Раздел";
</script>

<template>
  <div class="container">
    <div class="card stub">
      <h1 class="page-title">{{ title }}</h1>
      <p class="stub-text">Раздел находится в разработке.</p>
      <RouterLink class="btn btn-secondary" to="/products">
        Перейти к продукции
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.stub {
  padding: 18px;
}

.stub-text {
  margin: 10px 0 16px;
  color: var(--color-muted);
}
</style>

