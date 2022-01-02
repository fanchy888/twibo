<template>
  <el-container class="home">
    <el-header
      ><span class="logo">Twibo</span
      ><span class="head-btn" @click="logout">Logout</span>
    </el-header>

    <el-container>
      <el-aside>
        <el-col :span="20" style="height: 100%">
          <el-menu
            default-active="1"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            class="menu"
          >
            <el-menu-item index="1">
              <i class="el-icon-s-promotion"></i>
              <span slot="title" @click="jumpTo('twibo')">Twibo</span>
            </el-menu-item>
            <el-menu-item index="2">
              <i class="el-icon-s-comment"></i>
              <span slot="title" @click="jumpTo('uchat')">uChat</span>
            </el-menu-item>
            <el-menu-item index="3">
              <i class="el-icon-menu"></i>
              <span slot="title">uChat</span>
            </el-menu-item>
          </el-menu>
        </el-col>
      </el-aside>
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
    jumpTo(name) {
      this.$router.push({ name: name });
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
  line-height: 200px;
  height: 100%;
  width: 200px;
}

.el-main {
  background-color: #fffaf4;
  color: #333;
  text-align: center;
  line-height: 160px;
}
.menu {
  width: 200px;
  height: 100%;
}
</style>
