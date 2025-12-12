<script setup lang="ts">
import { computed } from "vue";

type DialogType = "error" | "warning" | "info" | "success";

const props = defineProps<{
  type: DialogType;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  showCancel?: boolean;
}>();

const emit = defineEmits<{
  confirm: [];
  cancel: [];
}>();

const icon = computed(() => {
  if (props.type === "error") {
    return "⛔";
  }
  if (props.type === "warning") {
    return "⚠";
  }
  if (props.type === "success") {
    return "✔";
  }
  return "ℹ";
});

const accent_class = computed(() => {
  if (props.type === "error") {
    return "dialog-error";
  }
  if (props.type === "warning") {
    return "dialog-warning";
  }
  if (props.type === "success") {
    return "dialog-success";
  }
  return "dialog-info";
});
</script>

<template>
  <div class="dialog-overlay" role="dialog" aria-modal="true">
    <div class="dialog card">
      <div class="dialog-header" :class="accent_class">
        <div class="dialog-title">
          <span class="dialog-icon" aria-hidden="true">{{ icon }}</span>
          <span>{{ title }}</span>
        </div>
      </div>
      <div class="dialog-body">
        <p class="dialog-message">{{ message }}</p>
      </div>
      <div class="dialog-actions">
        <button
          v-if="showCancel"
          class="btn btn-secondary"
          type="button"
          @click="emit('cancel')"
        >
          {{ cancelText ?? "Отмена" }}
        </button>
        <button class="btn btn-primary" type="button" @click="emit('confirm')">
          {{ confirmText ?? "Ок" }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.32);
  display: grid;
  place-items: center;
  padding: 20px;
  z-index: 50;
}

.dialog {
  width: min(560px, 100%);
  overflow: hidden;
}

.dialog-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border);
}

.dialog-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  font-size: 16px;
}

.dialog-icon {
  width: 24px;
  height: 24px;
  display: grid;
  place-items: center;
}

.dialog-body {
  padding: 16px;
}

.dialog-message {
  margin: 0;
  white-space: pre-wrap;
  color: var(--color-text);
  line-height: 1.4;
}

.dialog-actions {
  padding: 0 16px 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.dialog-error {
  background: rgba(176, 0, 32, 0.08);
}

.dialog-warning {
  background: rgba(154, 91, 0, 0.08);
}

.dialog-success {
  background: rgba(46, 125, 50, 0.08);
}

.dialog-info {
  background: rgba(53, 92, 189, 0.08);
}
</style>

