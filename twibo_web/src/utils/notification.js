import { Notification } from "element-ui";
import { isNil } from "./object";

export function showError(msg = "", dur) {
  Notification.error({
    title: "Error",
    message: msg,
    type: "error",
    duration: isNil(dur) ? 5000 : dur,
  });
}
export function showNotification(msg = "", title = "通知", dur) {
  Notification.success({
    title: title,
    message: msg,
    type: "success",
    duration: isNil(dur) ? 5000 : dur,
  });
}
