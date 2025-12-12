<template>
  <div class="container">
    <div class="card home">
      <h1 class="home-title">Подсистемы компании «Комфорт»</h1>
      <p class="home-text">
        Выберите раздел в меню слева. Для выполнения задания используется раздел
        «Продукция».
      </p>
      <RouterLink class="btn btn-primary home-btn" to="/products">
        Перейти к продукции
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 18px;
}

.home-title {
  margin: 0 0 8px;
  font-size: 22px;
  font-weight: 900;
}

.home-text {
  margin: 0 0 14px;
  color: var(--color-muted);
  line-height: 1.4;
}

.home-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
}
</style>

