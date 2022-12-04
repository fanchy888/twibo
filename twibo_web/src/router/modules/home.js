import home from "@/views/home";
import youChat from "@/components/uchat";
import twibo from "@/components/twibo";
import notes from "@/components/notes";
import setting from "@/components/setting";
import editTwibo from "@/components/twibo/edit";
import blog from "@/components/twibo/blogs";
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
          component: blog,
          name: "twibo",
        },
        {
          title: "edit",
          name: "edit",
          path: "edit",
          component: editTwibo,
          props: (route) => ({ query: route.query }),
        },
      ],
    },
    {
      title: "notes",
      name: "notes",
      path: "/notes",
      component: notes,
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
