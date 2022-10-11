import Vue from "vue";
import VueRouter from "vue-router";
import login from "../views/login";
import register from "../views/register";
import { makeRouteConfig } from "./helper";
import home from "./modules/home";

Vue.use(VueRouter);

const baseRoutes = [
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
  {
    path: "*",
    redirect: "/twibo",
  },
];

const allRoutes = [makeRouteConfig(home)];

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
  routes: [...baseRoutes, ...allRoutes],
});

router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    if (localStorage.getItem("token")) {
      next({ path: from.path });
    } else {
      next();
    }
  } else if (to.path === "/register") {
    next();
  } else {
    if (!localStorage.getItem("token")) {
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      });
    } else if (to.path === "/") {
      next({ path: "/twibo" });
    } else {
      next();
    }
  }
});

export default router;
