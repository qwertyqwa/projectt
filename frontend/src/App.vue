<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import AppFooter from "./components/AppFooter.vue";
import AppHeader from "./components/AppHeader.vue";
import AppSidebar from "./components/AppSidebar.vue";
import UiDialog from "./components/UiDialog.vue";
import { use_alert_state, use_confirm_state } from "./lib/dialog";

const route = useRoute();

const page_title = computed(() => {
  return (route.meta.title as string | undefined) ?? "Система";
});

const alert_state = use_alert_state();
const confirm_state = use_confirm_state();
</script>

<template>
  <div class="app-shell">
    <AppHeader :page-title="page_title" />
    <div class="app-body">
      <AppSidebar />
      <main class="app-main">
        <RouterView />
      </main>
    </div>
    <AppFooter />

    <UiDialog
      v-if="alert_state.open"
      :type="alert_state.type"
      :title="alert_state.title"
      :message="alert_state.message"
      :confirm-text="alert_state.confirm_text"
      @confirm="alert_state.on_confirm"
    />

    <UiDialog
      v-if="confirm_state.open"
      :type="confirm_state.type"
      :title="confirm_state.title"
      :message="confirm_state.message"
      :confirm-text="confirm_state.confirm_text"
      :cancel-text="confirm_state.cancel_text"
      show-cancel
      @confirm="confirm_state.on_confirm"
      @cancel="confirm_state.on_cancel"
    />
  </div>
</template>

