export default [
  {
    name: "getProjects",
    method: "GET",
    desc: "get projects",
    path: "/api/projects",
  },
  {
    name: "getOneProject",
    method: "GET",
    desc: "get projects",
    path: "/api/projects/:project_id",
  },
  {
    name: "createProject",
    method: "POST",
    desc: "create a project",
    path: "/api/projects",
  },
  {
    name: "deleteProject",
    method: "DELETE",
    desc: "delete a project",
    path: "/api/projects/:project_id",
  },
  {
    name: "updateProject",
    method: "PATCH",
    desc: "update a project",
    path: "/api/projects/:project_id",
  },

  {
    name: "createTask",
    method: "POST",
    desc: "create a project task",
    path: "/api/projects/:project_id/tasks",
  },
  {
    name: "getTasks",
    method: "GET",
    desc: "get project tasks",
    path: "/api/projects/:project_id/tasks",
  },
  {
    name: "updateTask",
    method: "PATCH",
    desc: "update a project task",
    path: "/api/projects/:project_id/tasks/:task_id",
  },
  {
    name: "deleteTasks",
    method: "DELETE",
    desc: "get project tasks",
    path: "/api/projects/:project_id/tasks/:task_id",
  },
];
