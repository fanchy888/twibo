<template>
  <el-card shadow="always" style="height: 100%; width: 100%">
    <el-container>
      <el-aside width="310px">
        <sideBar
          :friendList="friendList"
          :chatList="chatList"
          :friendRequests="friendRequests"
          :groupList="groupList"
        ></sideBar>
      </el-aside>
      <el-container>
        <el-main>
          <chatRoom v-if="currentChat.name" :chatInfo="currentChat"></chatRoom>
          <el-empty
            v-else
            :image-size="200"
            description="μChat is not WeChat"
          ></el-empty>
        </el-main>
      </el-container>
    </el-container>
  </el-card>
</template>
<script>
import { mapState, mapActions } from "vuex";
import sideBar from "./sidebar";
import chatRoom from "./chat";
export default {
  components: { sideBar, chatRoom },
  name: "youChat",
  data() {
    return {
      chat: {},
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendRequests: (state) => state.Friend.friendRequests,
      friendList: (state) => state.Friend.friendList,
      chatList: (state) => state.Chat.chatList,
      currentChat: (state) => state.Chat.currentChat,
      groupList: (state) => state.Chat.groupList,
    }),
  },
  // async mounted() {
  //   await this.getFriendRequests();
  //   await this.getFriends();
  //   await this.getChatList();
  // },
  methods: {
    ...mapActions([
      "getUserInfo",
      "getFriendRequests",
      "getFriends",
      "getChatList",
    ]),
  },
};
</script>
<style lang="scss" scoped></style>
