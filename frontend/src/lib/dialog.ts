import { reactive } from "vue";

type DialogType = "error" | "warning" | "info" | "success";

type AlertState = {
  open: boolean;
  type: DialogType;
  title: string;
  message: string;
  confirm_text: string;
  on_confirm: () => void;
};

type ConfirmState = {
  open: boolean;
  type: DialogType;
  title: string;
  message: string;
  confirm_text: string;
  cancel_text: string;
  on_confirm: () => void;
  on_cancel: () => void;
};

const alert_state = reactive<AlertState>({
  open: false,
  type: "info",
  title: "Информация",
  message: "",
  confirm_text: "Ок",
  on_confirm: () => {
    alert_state.open = false;
  },
});

const confirm_state = reactive<ConfirmState>({
  open: false,
  type: "warning",
  title: "Подтверждение",
  message: "",
  confirm_text: "Продолжить",
  cancel_text: "Отмена",
  on_confirm: () => {
    confirm_state.open = false;
  },
  on_cancel: () => {
    confirm_state.open = false;
  },
});

export function use_alert_state() {
  return alert_state;
}

export function use_confirm_state() {
  return confirm_state;
}

export function show_alert(type: DialogType, title: string, message: string) {
  alert_state.type = type;
  alert_state.title = title;
  alert_state.message = message;
  alert_state.confirm_text = "Ок";
  alert_state.on_confirm = () => {
    alert_state.open = false;
  };
  alert_state.open = true;
}

export function show_confirm(
  type: DialogType,
  title: string,
  message: string,
  confirm_text = "Продолжить",
  cancel_text = "Отмена"
) {
  return new Promise<boolean>((resolve) => {
    confirm_state.type = type;
    confirm_state.title = title;
    confirm_state.message = message;
    confirm_state.confirm_text = confirm_text;
    confirm_state.cancel_text = cancel_text;
    confirm_state.on_confirm = () => {
      confirm_state.open = false;
      resolve(true);
    };
    confirm_state.on_cancel = () => {
      confirm_state.open = false;
      resolve(false);
    };
    confirm_state.open = true;
  });
}

