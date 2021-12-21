import Vue from "vue";
import VueRouter from "vue-router";
import login from "../views/login";
import home from "../views/home";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: home,
    meta: { requireAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: login,
    meta: { keepalive: false },
  },
  {
    path: "/youchat",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    next();
  } else {
    if (!localStorage.getItem("token")) {
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  }
});

export default router;
