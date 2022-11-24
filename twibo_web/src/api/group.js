export default [
  {
    name: "getGroups",
    method: "GET",
    desc: "获取群列表",
    path: "/api/groups",
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
    name: "editGroups",
    method: "PATCH",
    desc: "编辑群",
    path: "/api/groups/:group_id",
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
