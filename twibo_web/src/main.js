import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import inject from "@/plugins/inject";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import VueSocketio from "vue-socket.io";

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(inject);
Vue.use(
  new VueSocketio({
    debug: true,
    connection: "http://localhost:5000/",
    /* 推荐使用vuex引入，方便多组件状态共享 */
    options: { path: "/test_conn" },
    vuex: {
      store,
      actionPrefix: "SOCKET_", // 前缀，为了区分vuex文件中响应函数和普通函数
    },
  })
);
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
