export default [
  {
    name: "getUserInfo",
    method: "GET",
    desc: "获取用户信息",
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
    path: "/api/user/search",
  },
  {
    name: "addFriend",
    method: "POST",
    desc: "加好友请求",
    path: "/api/user/:user_id/friend",
  },
  {
    name: "confirmFriend",
    method: "PATCH",
    desc: "接受好友请求",
    path: "/api/user/:user_id/friend",
  },
  {
    name: "getFriends",
    method: "GET",
    desc: "获取好友列表",
    path: "/api/user/:user_id/friends",
  },
  {
    name: "getFriendRequests",
    method: "GET",
    desc: "获取好友请求",
    path: "/api/user/:user_id/friend-request",
  },
  {
    name: "updateFriend",
    method: "PATCH",
    desc: "更新好友信息",
    path: "/user/:user_id/friend/:friend_user_id",
  },
  {
    name: "deleteFriend",
    method: "DELETE",
    desc: "删除好友",
    path: "/user/:user_id/friend/:friend_user_id",
  },
];
