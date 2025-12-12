<script setup lang="ts">
const nav_items = [
  { to: "/", label: "Главная" },
  { to: "/products", label: "Продукция" },
  { to: "/partners", label: "Партнеры" },
  { to: "/warehouse", label: "Склад и материалы" },
  { to: "/production", label: "Производство" },
  { to: "/staff", label: "Сотрудники" },
];
</script>

<template>
  <aside class="app-sidebar">
    <nav class="nav">
      <RouterLink
        v-for="item in nav_items"
        :key="item.to"
        class="nav-item"
        :to="item.to"
      >
        {{ item.label }}
      </RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.app-sidebar {
  width: 260px;
  background: var(--color-bg-secondary);
  border-right: 1px solid var(--color-border);
  padding: 14px;
}

.nav {
  display: grid;
  gap: 8px;
}

.nav-item {
  display: block;
  padding: 10px 12px;
  border-radius: 10px;
  font-weight: 800;
}

.nav-item.router-link-active {
  background: rgba(53, 92, 189, 0.14);
  color: var(--color-accent);
}
</style>

