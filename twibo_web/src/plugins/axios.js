import axios from "axios";
import { eventBus } from "@/utils/bus";
import { showError } from "@/utils/notification";

const axiosPromiseArr = [];
eventBus.$on("auth", () => {
  const { href, origin } = window.location;
  window.location.href = `${origin}/oauth2/?forward=${encodeURIComponent(
    href
  )}`;
});

eventBus.$on("toHome", () => {
  const { origin } = window.location;
  window.location.href = `${origin}/`;
});

function requestSuccessFunc(requestObj) {
  if (!requestObj.keep) {
    requestObj.cancelToken = new axios.CancelToken((cancel) => {
      axiosPromiseArr.push({ cancel });
    });
  }

  return requestObj;
}

function requestFailFunc(requestError) {
  return Promise.reject(requestError);
}

function responseSuccessFunc(responseObj) {
  // Status: 401 Unauthorized # 需要登录
  // Status: 400 Bad Request # 需要修改请求参数后提交
  // Status: 403 Forbidden
  // Status: 404 NotFound # 请求的资源链接不可用
  // Status: 409 app 注册 特殊code
  // Status: 412 系统只读状态，不可调用write相关接口
  // Status: 5XX Internal Server Error # 服务器内部错误
  const response = responseObj.data;
  const { data, meta } = response;
  const code = (meta && meta.code) || null;

  if (code === 200) {
    return data;
  }

  if (code === 401) {
    return eventBus.$emit("auth");
  }

  if (code === 404 && meta.error_message === "App Group not exist") {
    return eventBus.$emit("toHome");
  }

  if (meta && meta.code >= 500) {
    return Promise.reject((meta && meta) || "error");
  }

  if ((meta && meta.error_message) || (meta && meta.code !== 409)) {
    if (meta.code === 412) {
      showError(meta.error_message);
    } else {
      showError(meta.error_message, 0);
    }
  }

  return Promise.reject((meta && meta) || "error");
}

function responseFailFunc(responseError) {
  if (responseError.toString && responseError.toString() !== "Cancel") {
    if (responseError.message) {
      if (responseError.message === "Request failed with status code 504") {
        showError("Request Timeout", 0);
      } else {
        showError(responseError.response.data.msg, 0);
      }
    }
  }

  return Promise.reject(
    responseError.response || responseError.message || "Error"
  );
}

const AXIOS_DEFAULT_CONFIG = {
  baseURL: "/api",
  // timeout: 50000
};
const axiosInstance = axios.create(AXIOS_DEFAULT_CONFIG);

axiosInstance.interceptors.request.use(requestSuccessFunc, requestFailFunc);
axiosInstance.interceptors.response.use(responseSuccessFunc, responseFailFunc);

export default axiosInstance;
