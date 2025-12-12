<script setup lang="ts">
defineProps<{
  pageTitle: string;
}>();
</script>

<template>
  <header class="app-header">
    <div class="app-header-left">
      <img class="app-logo" src="/logo.png" alt="Логотип компании Комфорт" />
      <div class="app-header-text">
        <div class="app-org">Комфорт</div>
        <div class="app-page">{{ pageTitle }}</div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 72px;
  background: var(--color-bg-secondary);
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--color-border);
}

.app-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-logo {
  width: 44px;
  height: 44px;
  object-fit: contain;
}

.app-header-text {
  display: grid;
  line-height: 1.1;
}

.app-org {
  font-size: 18px;
  font-weight: 900;
}

.app-page {
  font-size: 14px;
  color: var(--color-muted);
  font-weight: 700;
}
</style>

