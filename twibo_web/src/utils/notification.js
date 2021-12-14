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
