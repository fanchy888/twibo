<template>
  <el-card shadow="always" style="height: 100%">
    <el-container class="uchat">
      <el-aside width="300px">
        <sideBar @joinChat="joinChat"></sideBar>
      </el-aside>
      <el-container>
        <el-main><chatRoom :chatInfo="chat"></chatRoom></el-main>
      </el-container>
    </el-container>
  </el-card>
</template>
<script>
import sideBar from "./sidebar";
import chatRoom from "./chat";
export default {
  components: { sideBar, chatRoom },
  name: "youChat",
  data() {
    return {
      chat: { name: "test" },
    };
  },
  methods: {
    joinChat(chat) {
      this.chat = chat;
    },
  },
};
</script>
<style lang="scss" scoped></style>
