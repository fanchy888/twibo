<template>
  <el-container class="home">
    <el-header
      ><span class="logo">Twibo</span>
      <span class="head-btn">
        <el-dropdown trigger="click">
          <div class="avatar">
            <el-avatar v-if="user && user.avatar" :size="40" :src="avatarUrl" />
            <i v-else class="el-icon-picture-outline"></i>
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>
              <span @click="jumpTo('setting')"
                ><i class="el-icon-setting"></i>Settings</span
              >
            </el-dropdown-item>
            <el-dropdown-item>
              <span @click="logout"><i class="el-icon-ship"></i>Logout</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </span>
    </el-header>

    <el-container>
      <el-aside>
        <el-col :span="20" style="height: 100%">
          <el-menu
            default-active="twibo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            class="menu"
            router
          >
            <el-menu-item index="twibo">
              <i class="el-icon-s-promotion"></i>
              <span slot="title">Twibo</span>
            </el-menu-item>
            <el-menu-item index="uchat">
              <i class="el-icon-s-comment"></i>
              <span slot="title">uChat</span>
            </el-menu-item>
            <el-menu-item index="">
              <i class="el-icon-edit"></i>
              <span slot="title">Notes</span>
            </el-menu-item>
          </el-menu>
        </el-col>
      </el-aside>
      <el-main><router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>

<script>
import { mapActions } from "vuex";
import { currentUser } from "@/utils/user";
export default {
  name: "Home",
  data() {
    return {
      message: "",
    };
  },
  computed: {
    user() {
      return currentUser();
    },
    avatarUrl() {
      return this.$staticUrl + this.user.avatar;
    },
  },
  mounted() {
    if (!this.$store.state.Socket.isConnected) {
      this.$socket.open();
    }
    this.sockets.subscribe("message", (data) => {
      console.log(data);
    });
    this.getUserInfo();
  },
  methods: {
    ...mapActions(["getUserInfo"]),
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
      const routeParam = { name: name };
      this.$router.push(routeParam);
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
  height: 70px !important;
  line-height: 70px;
}
.logo {
  color: #ececea;
  font-family: "PingFang SC";
  font-size: 30px;
  font-weight: 600;
  text-shadow: -4px 6px 3px #060606;
}
.head-btn {
  float: right;
  height: 70px;
  .el-dropdown {
    font-size: 30px;
    color: #ececea;
  }
  .avatar {
    padding: 10px;
    height: 70px;
  }
  .avatar :hover {
    cursor: pointer;
  }
}

.el-aside {
  line-height: 200px;
  height: 100%;
  width: 200px !important;
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
