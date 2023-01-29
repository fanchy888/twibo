import home from "@/views/home";
import youChat from "@/components/uchat";
import twibo from "@/components/twibo";
import ByteTok from "@/components/ByteTok";
import setting from "@/components/setting";
import editTwibo from "@/components/twibo/edit";
import blogs from "@/components/twibo/blogs";
import blogPage from "@/components/twibo/blog";
export default {
  title: "home",
  icon: "home",
  path: "",
  component: home,
  props: (route) => ({ query: route.query }),
  children: [
    {
      title: "uchat",
      name: "uchat",
      path: "/uchat",
      component: youChat,
      props: (route) => ({ query: route.query }),
    },
    {
      title: "twibo",
      path: "/twibo",
      component: twibo,
      props: (route) => ({ query: route.query }),
      children: [
        {
          path: "",
          component: blogs,
          name: "twibo",
        },
        {
          title: "edit",
          name: "edit",
          path: "edit",
          component: editTwibo,
          props: (route) => ({ query: route.query }),
        },
        {
          title: "editBlog",
          name: "editBlog",
          path: "edit/:blog_id",
          component: editTwibo,
          props: (route) => ({ query: route.query }),
        },
        {
          title: "blogPage",
          name: "blogPage",
          path: ":blog_id",
          component: blogPage,
          props: (route) => ({ query: route.query }),
        },
      ],
    },
    {
      title: "bytetok",
      name: "bytetok",
      path: "/bytetok",
      component: ByteTok,
      props: (route) => ({ query: route.query }),
    },
    {
      title: "setting",
      name: "setting",
      path: "setting",
      component: setting,
      props: (route) => ({ query: route.query }),
    },
  ],
};
