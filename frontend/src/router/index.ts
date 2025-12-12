import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../pages/HomePage.vue";
import ProductFormPage from "../pages/ProductFormPage.vue";
import ProductWorkshopsPage from "../pages/ProductWorkshopsPage.vue";
import ProductsPage from "../pages/ProductsPage.vue";
import StubPage from "../pages/StubPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
      meta: { title: "Главная" },
    },
    {
      path: "/products",
      name: "products",
      component: ProductsPage,
      meta: { title: "Продукция" },
    },
    {
      path: "/products/new",
      name: "product-new",
      component: ProductFormPage,
      meta: { title: "Добавление продукции" },
    },
    {
      path: "/products/:id",
      name: "product-edit",
      component: ProductFormPage,
      meta: { title: "Редактирование продукции" },
    },
    {
      path: "/products/:id/workshops",
      name: "product-workshops",
      component: ProductWorkshopsPage,
      meta: { title: "Цеха производства" },
    },
    {
      path: "/partners",
      name: "partners",
      component: StubPage,
      meta: { title: "Партнеры" },
    },
    {
      path: "/warehouse",
      name: "warehouse",
      component: StubPage,
      meta: { title: "Склад и материалы" },
    },
    {
      path: "/production",
      name: "production",
      component: StubPage,
      meta: { title: "Производство" },
    },
    {
      path: "/staff",
      name: "staff",
      component: StubPage,
      meta: { title: "Сотрудники" },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: StubPage,
      meta: { title: "Страница не найдена" },
    },
  ],
});

router.afterEach((to) => {
  const title = (to.meta.title as string | undefined) ?? "Система";
  document.title = `Комфорт — ${title}`;
});
