import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../pages/HomePage.vue";
import EmployeeFormPage from "../pages/EmployeeFormPage.vue";
import MaterialFormPage from "../pages/MaterialFormPage.vue";
import PartnerFormPage from "../pages/PartnerFormPage.vue";
import PartnersPage from "../pages/PartnersPage.vue";
import ProductFormPage from "../pages/ProductFormPage.vue";
import ProductWorkshopsPage from "../pages/ProductWorkshopsPage.vue";
import ProductsPage from "../pages/ProductsPage.vue";
import ProductionPage from "../pages/ProductionPage.vue";
import StaffPage from "../pages/StaffPage.vue";
import StubPage from "../pages/StubPage.vue";
import SupplierFormPage from "../pages/SupplierFormPage.vue";
import WarehousePage from "../pages/WarehousePage.vue";
import WorkshopFormPage from "../pages/WorkshopFormPage.vue";

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
      component: PartnersPage,
      meta: { title: "Партнеры" },
    },
    {
      path: "/partners/new",
      name: "partner-new",
      component: PartnerFormPage,
      meta: { title: "Добавление партнера" },
    },
    {
      path: "/partners/:id",
      name: "partner-edit",
      component: PartnerFormPage,
      meta: { title: "Редактирование партнера" },
    },
    {
      path: "/warehouse",
      name: "warehouse",
      component: WarehousePage,
      meta: { title: "Склад и материалы" },
    },
    {
      path: "/warehouse/suppliers/new",
      name: "supplier-new",
      component: SupplierFormPage,
      meta: { title: "Добавление поставщика" },
    },
    {
      path: "/warehouse/suppliers/:id",
      name: "supplier-edit",
      component: SupplierFormPage,
      meta: { title: "Редактирование поставщика" },
    },
    {
      path: "/warehouse/materials/new",
      name: "material-new",
      component: MaterialFormPage,
      meta: { title: "Добавление материала" },
    },
    {
      path: "/warehouse/materials/:id",
      name: "material-edit",
      component: MaterialFormPage,
      meta: { title: "Редактирование материала" },
    },
    {
      path: "/production",
      name: "production",
      component: ProductionPage,
      meta: { title: "Производство" },
    },
    {
      path: "/production/workshops/new",
      name: "workshop-new",
      component: WorkshopFormPage,
      meta: { title: "Добавление цеха" },
    },
    {
      path: "/production/workshops/:id",
      name: "workshop-edit",
      component: WorkshopFormPage,
      meta: { title: "Редактирование цеха" },
    },
    {
      path: "/staff",
      name: "staff",
      component: StaffPage,
      meta: { title: "Сотрудники" },
    },
    {
      path: "/staff/new",
      name: "employee-new",
      component: EmployeeFormPage,
      meta: { title: "Добавление сотрудника" },
    },
    {
      path: "/staff/:id",
      name: "employee-edit",
      component: EmployeeFormPage,
      meta: { title: "Редактирование сотрудника" },
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
