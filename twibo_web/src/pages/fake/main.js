import Vue from "vue";
import App from "./App.vue";
import "../../registerServiceWorker";

import inject from "@/plugins/inject";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import router from "./router";
import VueCookies from "vue-cookies";
Vue.config.productionTip = false;

Vue.use(ElementUI);
Vue.use(inject);
Vue.use(VueCookies);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#fake");
