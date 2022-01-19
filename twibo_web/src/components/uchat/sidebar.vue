<template>
  <div class="side">
    <div class="search">
      <el-input
        prefix-icon="el-icon-search"
        v-model="searchInfo"
        placeholder="搜索"
      ></el-input>
    </div>
    <el-tabs
      v-model="activeName"
      type="border-card"
      @tab-click="handleClick"
      stretch
    >
      <el-tab-pane name="chat">
        <span slot="label" style="font-size: 20px"
          ><i class="el-icon-chat-line-round"></i
        ></span>
        <div class="chat">
          <div
            v-for="(chat, index) in chatList"
            :key="index.toString()"
            class="chat-item"
          >
            <el-avatar
              v-if="chat.avatar"
              :src="avatarSrc(chat.avatar)"
              :size="40"
              shape="square"
            ></el-avatar>
            <el-avatar v-else :size="40" shape="square">
              <span style="font-size: 30px"><i class="el-icon-user"></i></span>
            </el-avatar>
            <div class="chat-item-info">
              <div class="chat-item-name">
                <div class="name">{{ chat.name }}</div>
              </div>
              <div class="chat-item-msg">
                <div class="msg">{{ chat.lastMsg }}</div>
                <div class="time">{{ chat.time }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane name="friend">
        <span slot="label" style="font-size: 20px"
          ><i class="el-icon-user-solid"></i
        ></span>
        <div class="chat">
          <div class="add">
            <el-button icon="el-icon-plus" @click="addVisible = true"
              >添加好友</el-button
            >
          </div>
          <div
            v-for="(friend, index) in friendList"
            :key="index.toString()"
            class="chat-item"
          >
            <el-avatar
              v-if="friend.avatar"
              :src="avatarSrc(friend.avatar)"
              :size="40"
            ></el-avatar>
            <el-avatar v-else :size="40">
              <span style="font-size: 30px"><i class="el-icon-user"></i></span>
            </el-avatar>
            <div class="friend">{{ friend.name }}</div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    <el-dialog width="30%" :visible.sync="addVisible">
      <div class="search">
        <el-input
          prefix-icon="el-icon-search"
          v-model="searchUser"
          placeholder="搜一搜"
          @change="getUser"
        ></el-input>
      </div>
      <div class="search-result">No Result</div>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "sideBar",
  data() {
    return {
      activeName: "chat",
      chatList: [],
      friendList: ["a", "b"],
      searchInfo: "",
      addVisible: false,
      searchUser: "",
    };
  },
  mounted() {
    this.chatList.push({
      avatar: "avatar.jpg",
      name: "test",
      lastMsg: "nihaoaaaaaaaaaaaaaaaaaaaaaaa",
      time: "19:20",
    });
    this.chatList.push({
      avatar: "",
      name: "test2",
      lastMsg: "",
      time: "",
    });
    this.friendList = [
      ...this.chatList,
      ...this.chatList,
      ...this.chatList,
      ...this.chatList,
      ...this.chatList,
      ...this.chatList,
      ...this.chatList,
      ...this.chatList,
    ];
  },
  methods: {
    handleClick() {},
    avatarSrc(avatar) {
      return this.$staticUrl + avatar;
    },
    getUser(val) {
      console.log(val);
    },
  },
};
</script>
<style lang="scss" scoped>
.side {
  height: 600px;
  padding: 10px 10px;
  border-right: 1px solid #eaecf1;
}
.search {
  height: 50px;
  line-height: 50px;
  margin: auto;
}
.chat {
  height: 450px;
  overflow-y: auto;
}
.chat-item {
  width: auto;
  height: 50px;
  line-height: 50px;
  display: flex;
  align-items: center;
  border-bottom: solid 1px #eaecf1;
}
.chat-item:hover {
  background: #ececea;
}
.chat-item-info {
  padding-left: 7px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.chat-item-name {
  height: 20px;
  line-height: 20px;
  font-size: 18px;
  font-weight: 600;
  color: rgb(84, 92, 100);
}
.chat-item-msg {
  height: 20px;
  line-height: 20px;
  display: flex;
  justify-content: space-between;
  width: 200px;
  .time {
    font-size: 10px;
    color: #a6a6a8;
  }
  .msg {
    font-size: 10px;
    width: 100px;
    color: #a6a6a8;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
}
.friend {
  padding-left: 10px;
  font-size: 20px;
  color: rgb(84, 92, 100);
  font-weight: 600;
}
.add {
  display: flex;
  justify-content: center;
  padding-bottom: 10px;
  border-bottom: solid 1px #eaecf1;
}
</style>
