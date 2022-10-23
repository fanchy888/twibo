import Vue from "vue";
import VueRouter from "vue-router";
import jump from "./components/jump";
Vue.use(VueRouter);

const routes = [
  {
    path: "/jump",
    name: "jump",
    component: jump,
    meta: { keepalive: false },
  },
];

const router = new VueRouter({
  mode: "history",
  base: "/",
  routes: [...routes],
});

export default router;
