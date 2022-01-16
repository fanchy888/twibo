import home from "@/views/home";
import youChat from "@/components/uchat";
import twibo from "@/components/twibo";
import setting from "@/components/setting";
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
      path: "uchat",
      component: youChat,
      props: (route) => ({ query: route.query }),
    },
    {
      title: "twibo",
      name: "twibo",
      path: "twibo",
      component: twibo,
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
