export default [
  {
    name: "getUserInfo",
    method: "GET",
    desc: "测试接口1",
    path: "/api/user",
  },
  {
    name: "register",
    method: "POST",
    desc: "register",
    path: "/api/register",
  },
  {
    name: "login",
    method: "POST",
    desc: "login",
    path: "/api/login",
  },
  {
    name: "logout",
    method: "GET",
    desc: "logout",
    path: "/api/logout",
  },
  {
    name: "upload",
    method: "POST",
    path: "/api/upload",
  },
  {
    name: "updateUserInfo",
    method: "PATCH",
    path: "/api/user",
  },
  {
    name: "getUserByName",
    method: "GET",
    desc: "搜索",
    path: "/api/user/friend",
  },
  {
    name: "addFriend",
    method: "POST",
    desc: "加好友请求",
    path: "/api/user/friend",
  },
  {
    name: "confirmFriend",
    method: "PATCH",
    desc: "接受好友请求",
    path: "/api/user/friend/:user_id",
  },
];
