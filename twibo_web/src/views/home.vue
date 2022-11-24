<template>
  <el-container class="home">
    <el-header
      ><span class="logo">Twibo</span>
      <span class="head-btn">
        <el-dropdown trigger="click" class="avatar">
          <el-avatar
            v-if="user && user.avatar"
            :size="40"
            :src="avatarSrc(user.avatar)"
            class="ava-child"
            fit="contain"
          />
          <el-avatar v-else :size="40" icon="el-icon-user" class="ava-child">
          </el-avatar>

          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>
              <span @click="jumpTo('setting')"
                ><i class="el-icon-setting"></i>Settings</span
              >
            </el-dropdown-item>
            <el-dropdown-item>
              <span @click="logout"><i class="el-icon-ship"></i>Sign Out</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </span>
    </el-header>

    <el-container>
      <el-aside>
        <el-col :span="20" style="height: 100%">
          <el-menu
            :default-active="active"
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
              <span slot="title">μChat</span>
            </el-menu-item>
            <el-menu-item index="notes">
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
import { mapActions, mapState } from "vuex";
import { avatarSrc } from "@/utils/common";
export default {
  name: "Home",
  data() {
    return {
      message: "",
      active: "twibo",
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
  },
  async mounted() {
    if (!this.$store.state.Socket.isConnected) {
      this.$socket.open();
    }
    if (!this.user) {
      await this.getUserInfo();
    }
    if (this.user.user_id) {
      await this.getFriendRequests();
      await this.getFriends();
      await this.getChatList();
      await this.getGroups();
      this.active = this.$route.name;
    }
  },

  methods: {
    ...mapActions([
      "getUserInfo",
      "getFriendRequests",
      "getFriends",
      "getChatList",
      "getGroups",
    ]),
    avatarSrc: avatarSrc,
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
  // font-family: "PingFang SC";
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
    width: 70px;
  }
  .avatar :hover {
    cursor: pointer;
    box-shadow: 0 0 1px 2px #fdf9ee;
  }
  .ava-child :hover {
    box-shadow: unset;
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
