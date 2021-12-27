import Vue from "vue";
import VueRouter from "vue-router";
import login from "../views/login";
import register from "../views/register";
import home from "../views/home";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: home,
  },
  {
    path: "/login",
    name: "login",
    component: login,
    meta: { keepalive: false },
  },
  {
    path: "/register",
    name: "register",
    component: register,
  },
];

["push", "replace"].forEach((k) => {
  const originalFn = VueRouter.prototype[k];
  VueRouter.prototype[k] = function (location, onResolve, onReject) {
    if (onResolve || onReject) {
      return originalFn.call(this, location, onResolve, onReject);
    }
    return originalFn.call(this, location).catch((err) => err);
  };
});

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    if (sessionStorage.getItem("token")) {
      next({ path: from.path });
    } else {
      next();
    }
  } else if (to.path === "/register") {
    next();
  } else {
    if (!sessionStorage.getItem("token")) {
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
