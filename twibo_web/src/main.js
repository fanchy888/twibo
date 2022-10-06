import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import inject from "@/plugins/inject";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import VueSocketio from "vue-socket.io";
import socketIO from "socket.io-client";
import JSEncrypt from "jsencrypt";
import { rsaPublicKey } from "./rsa";
import { staticUrl } from "@/utils/common";
Vue.config.productionTip = false;

Vue.prototype.$getRsaCode = function (str) {
  let pubKey = rsaPublicKey;
  let encryptStr = new JSEncrypt();
  encryptStr.setPublicKey(pubKey);
  let data = encryptStr.encrypt(str.toString());
  return data;
};

Vue.prototype.$staticUrl = staticUrl;

Vue.use(ElementUI);
Vue.use(inject);
Vue.use(
  new VueSocketio({
    debug: true,
    connection: socketIO("http://192.168.5.2:5000/twibo", {
      transports: ["websocket"],
      autoConnect: false,
      reconnection: true,
    }),
    options: { autoConnect: false },
    vuex: {
      store,
      actionPrefix: "SOCKET_",
      mutationPrefix: "SOCKET_",
    },
  })
);
new Vue({
  router,
  store,
  sockets: {
    connect() {
      console.log("connected");
    },
    disconnect() {
      console.log("disconnected");
    },
  },
  render: (h) => h(App),
}).$mount("#app");
