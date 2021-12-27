import Home from "@/views/home.vue";

export const makePath = (title) => {
  return title
    .toLowerCase() // 1. 处理大小写
    .replace(/\(.*\)/g, "") // 2. 括号以及内部内容剔除
    .replace(/^(\W)*|(\W)*$/g, "") // 3. 前非字符处理
    .replace(/\W/g, "_") //4. 非字符转_
    .replace(/_+/g, "_"); //5. 多个_转成一个_
};

export const makeRouteConfig = (obj) => {
  const path = obj.path || makePath(obj.title);
  const res = {
    name: obj.title + 1,
    path: path,
    meta: {
      title: obj.title,
      icon: obj.icon,
      roles: (obj.meta || {}).roles || null,
    },
    component: Home,
    redirect: {
      name: pointer(obj).children[0].children[0].children[0].name(""),
    },
  };
  // res.children = obj.children.map((o2) => {
  //   const res2 = {
  //     name: o2.title + 2,
  //     path: o2.path || makePath(o2.title),
  //     meta: {
  //       title: o2.title,
  //       isExternal: !!o2.path,
  //       oldPath: o2.path,
  //     },
  //   };
  //   res2.redirect = {
  //     name: pointer(o2).children[0].children[0].name(),
  //   };
  //   res2.component = NavMenu;

  //   res2.children =
  //     o2.children &&
  //     o2.children.map((o3) => ({
  //       name: o2.title + o3.title + 3,
  //       path: o3.path || makePath(o3.title),
  //       meta: {
  //         title: o3.title,
  //         isExternal: !!o3.path,
  //         oldPath: o3.path,
  //       },
  //       component: BreadCrumb,
  //       redirect: {
  //         name: pointer(o3).children[0].name(),
  //       },
  //       children: o3.children,
  //     }));

  //   return res2;
  // });

  return res;
};

/* =====================================
链式取值 如 res.data.goods.list[0].price
数据不全导致报错：Uncaught TypeError: Cannot read property 'goods' of undefined
使用：pointer(res).data.goods.list[0].price(666) 666为默认值
===================================== */
export const pointer = (obj, path = []) => {
  return new Proxy(() => {}, {
    get(target, property) {
      return pointer(obj, path.concat(property));
    },
    apply(target, self, args) {
      let val = obj;
      // let parent
      for (let i = 0; i < path.length; i++) {
        if (val === null || val === undefined) {
          break;
        }
        // parent = val
        val = val[path[i]];
      }
      if (val === null || val === undefined) {
        val = args[0];
      }
      return val;
    },
  });
};
