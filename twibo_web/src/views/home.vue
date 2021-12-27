<template>
  <el-container class="home">
    <el-header
      ><span class="logo">Twibo</span
      ><span class="head-btn" @click="logout">Logout</span></el-header
    >

    <el-container>
      <el-aside width="200px">Aside</el-aside>
      <el-main><router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      message: "",
    };
  },
  mounted() {
    if (!this.$store.state.Socket.isConnected) {
      this.$socket.open();
    }
    this.sockets.subscribe("message", (data) => {
      console.log(data);
    });
  },
  methods: {
    sendMessage(data) {
      this.$socket.emit("message", data);
    },
    getReply(data) {
      this.$socket.emit("auto_reply", data);
    },
    async logout() {
      await this.$api.logout();
      this.$store.commit("logout");
      this.$router.push("/login");
    },
  },
};
</script>
<style lang="scss" scoped>
.home {
  background-color: #fffaf4;
  height: 100%;
  width: 100%;
}
.el-header {
  background-color: #2c3e50;
  text-align: center;
  height: 80px !important;
  line-height: 80px;
}
.logo {
  color: #ececea;
  font-family: "PingFang SC";
  font-size: 30px;
  font-weight: 600;
  text-shadow: -4px 6px 3px #060606;
}
.head-btn {
  color: #ececea;
  float: right;
  font-size: 14px;
  margin-top: 20px;
}
.head-btn:hover {
  color: #d3dce6;
  cursor: pointer;
}
.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #fffaf4;
  color: #333;
  text-align: center;
  line-height: 160px;
}
</style>
