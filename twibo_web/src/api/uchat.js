export default [
  {
    name: "getChatList",
    method: "GET",
    desc: "获取用户聊天列表",
    path: "/api/chats",
  },
  {
    name: "uploadChatImg",
    method: "POST",
    desc: "发图片",
    path: "/api/chats/:chat_id/img",
  },
];
