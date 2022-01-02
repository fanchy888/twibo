export const makePath = (title) => {
  if (title === "home") {
    return "";
  }
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
    name: obj.name,
    path: "/" + path,
    meta: {
      title: obj.title,
      icon: obj.icon,
      roles: (obj.meta || {}).roles || null,
    },
    component: obj.component,
  };
  res.children = obj.children.map((o2) => {
    const res2 = {
      name: o2.name,
      path: o2.path || makePath(o2.title),
      meta: {
        title: o2.title,
        isExternal: !!o2.path,
        oldPath: o2.path,
      },
    };
    res2.component = o2.component;
    return res2;
  });
  return res;
};
