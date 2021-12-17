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
Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(inject);
Vue.use(
  new VueSocketio({
    debug: true,
    connection: socketIO("http://localhost:5000/test_conn", {
      transports: ["websocket"],
    }),

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
  render: (h) => h(App),
}).$mount("#app");
