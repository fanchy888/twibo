export default [
  {
    name: "getGroups",
    method: "GET",
    desc: "获取群列表",
    path: "/api/groups",
  },
  {
    name: "getOneGroup",
    method: "GET",
    desc: "获取一个群",
    path: "/api/groups/:group_id",
  },
  {
    name: "createGroup",
    method: "POST",
    desc: "建群",
    path: "/api/groups",
  },
  {
    name: "deleteGroup",
    method: "DELETE",
    desc: "删群",
    path: "/api/groups/:group_id",
  },
  {
    name: "editGroup",
    method: "PATCH",
    desc: "编辑群",
    path: "/api/groups/:group_id",
  },
  {
    name: "editGroupAvatar",
    method: "POST",
    desc: "编辑群头像",
    path: "/api/groups/:group_id/avatar",
  },
  {
    name: "addGroupMember",
    method: "POST",
    desc: "加人",
    path: "/api/groups/:group_id/members",
  },
  {
    name: "kickGroupMember",
    method: "DELETE",
    desc: "踢人",
    path: "/api/groups/:group_id/members",
  },
];
