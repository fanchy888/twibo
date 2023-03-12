export default [
  {
    name: "uploadBlogImage",
    method: "POST",
    desc: "上传图片",
    path: "/api/blogs/image",
  },
  {
    name: "createBlog",
    method: "POST",
    desc: "创建blog",
    path: "/api/blogs",
  },
  {
    name: "updateBlog",
    method: "PATCH",
    desc: "创建blog",
    path: "/api/blogs/:blog_id",
  },
  {
    name: "deleteBlog",
    method: "DELETE",
    desc: "创建blog",
    path: "/api/blogs/:blog_id",
  },
  {
    name: "getBlogs",
    method: "GET",
    desc: "获取blog",
    path: "/api/blogs",
  },
  {
    name: "getOneBlog",
    method: "GET",
    desc: "获取blog列表",
    path: "/api/blogs/:blog_id",
  },
];
