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
            v-for="(chat, index) in filterdChatList"
            :key="index.toString()"
            class="chat-item"
            @click="read(chat)"
          >
            <el-badge is-dot style="height: 40px" :hidden="!chat.new">
              <el-avatar
                v-if="chat.avatar"
                :src="avatarSrc(chat.avatar)"
                :size="40"
                shape="square"
              ></el-avatar>
              <el-avatar v-else :size="40" shape="square">
                <span style="font-size: 30px"
                  ><i class="el-icon-user"></i
                ></span>
              </el-avatar>
            </el-badge>
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
        <div class="chat" v-loading="loading">
          <div class="add">
            <el-button icon="el-icon-plus" @click="addVisible = true"
              >添加好友</el-button
            >
          </div>
          <el-collapse v-model="activeFriend">
            <el-collapse-item name="request" title="新的朋友">
              <template slot="title"
                >新的朋友
                <el-badge
                  :value="friendRequests.length"
                  :max="99"
                  :hidden="!friendRequests.length"
                ></el-badge>
              </template>
              <div
                v-for="(friend, index) in friendRequests"
                :key="index.toString()"
                class="request-item"
              >
                <div class="info">
                  <el-avatar
                    v-if="friend.avatar"
                    :src="avatarSrc(friend.avatar)"
                    :size="40"
                  ></el-avatar>
                  <el-avatar v-else :size="40">
                    <span style="font-size: 30px"
                      ><i class="el-icon-user"></i
                    ></span>
                  </el-avatar>
                  <div class="friend">
                    <span style="text-overflow: ellipsis; overflow: hidden">{{
                      friend.name
                    }}</span>
                  </div>
                </div>
                <div>
                  <el-button
                    type="success"
                    size="mini"
                    plain
                    @click="confirmFriend(friend)"
                    >接受</el-button
                  >
                  <el-button
                    type="danger"
                    size="mini"
                    plain
                    @click="rejectFriend(friend)"
                    >拒绝</el-button
                  >
                </div>
              </div>
            </el-collapse-item>
            <el-collapse-item name="friend" title="好友">
              <div
                v-for="(friend, index) in filterdFriends"
                :key="index.toString()"
                class="chat-item"
              >
                <el-avatar
                  v-if="friend.avatar"
                  :src="avatarSrc(friend.avatar)"
                  :size="40"
                ></el-avatar>
                <el-avatar v-else :size="40">
                  <span style="font-size: 30px"
                    ><i class="el-icon-user"></i
                  ></span>
                </el-avatar>
                <div class="friend">
                  <span style="text-overflow: ellipsis; overflow: hidden">{{
                    friend.nick_name || friend.name
                  }}</span>
                  <el-popover placement="right">
                    <el-button
                      slot="reference"
                      icon="el-icon-edit"
                      circle
                    ></el-button>
                  </el-popover>
                </div></div
            ></el-collapse-item>
          </el-collapse>
        </div>
      </el-tab-pane>
    </el-tabs>
    <el-dialog width="30%" :visible.sync="addVisible">
      <div class="search">
        <el-input
          prefix-icon="el-icon-search"
          v-model="searchUserText"
          placeholder="搜一搜"
          @change="getUserByName"
          maxlength="50"
        ></el-input>
      </div>
      <div class="search-result" v-loading="dloading">
        <div v-if="searchResult" class="item">
          <div class="left">
            <el-avatar
              v-if="searchResult.avatar"
              :src="avatarSrc(searchResult.avatar)"
              :size="80"
            ></el-avatar>
            <el-avatar v-else :size="80">
              <span style="font-size: 50px"><i class="el-icon-user"></i></span>
            </el-avatar>
          </div>
          <div class="right">
            <div class="result-name">
              {{ searchResult.name }}
            </div>
            <div class="result-des">
              {{ searchResult.description }}
            </div>
            <el-button type="success" size="medium" @click="addFriend"
              >Add</el-button
            >
          </div>
        </div>
        <div v-else>无结果</div>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "sideBar",
  data() {
    return {
      activeName: "chat",
      activeFriend: ["friend"],
      chatList: [],
      searchInfo: "",
      addVisible: false,
      searchUserText: "",
      searchResult: null,
      dloading: false,
      loading: false,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendRequests: (state) => state.Friend.friendRequests,
      friendList: (state) => state.Friend.friendList,
    }),
    filterdFriends() {
      return this.friendList.filter(
        (f) =>
          (f.nick_name && f.nick_name.includes(this.searchInfo)) ||
          f.name.includes(this.searchInfo)
      );
    },
    filterdChatList() {
      return this.chatList.filter((f) => f.name.includes(this.searchInfo));
    },
  },
  async mounted() {
    this.chatList.push({
      avatar: "avatar.jpg",
      name: "test",
      lastMsg: "nihaoaaaaaaaaaaaaaaaaaaaaaaa",
      time: "19:20",
      nick_name: "nick_1",
      new: true,
    });
    this.chatList.push({
      avatar: "",
      name: "test2",
      lastMsg: "",
      time: "",
    });

    if (!this.user) {
      await this.getUserInfo();
    }
    await this.getFriendRequests();
    await this.getFriends();
  },
  methods: {
    ...mapActions(["getUserInfo", "getFriendRequests", "getFriends"]),
    handleClick() {},
    avatarSrc(avatar) {
      return this.$staticUrl + avatar;
    },

    read(chat) {
      chat.new = false;
    },
    async getUserByName(name) {
      if (!name) {
        return;
      }
      try {
        this.dloading = true;
        const user = await this.$api.getUserByName({ name: name });
        this.searchResult = user;
      } finally {
        this.dloading = false;
      }
    },
    async addFriend() {
      this.dloading = true;
      try {
        await this.$api.addFriend({ user_id: this.searchResult.user_id });
      } finally {
        this.dloading = false;
        this.addVisible = false;
        this.searchUserText = "";
        this.searchResult = null;
      }
    },

    async confirmFriend(friend) {
      this.loading = true;
      try {
        const params = {
          user_id: this.user.user_id,
          $query: {
            friend_id: friend.user_id,
          },
        };
        await this.$api.confirmFriend(params);
      } finally {
        this.loading = false;
      }
    },

    async rejectFriend(friend) {
      this.loading = true;
      try {
        const params = {
          user_id: this.user.user_id,
          $query: {
            friend_id: friend.user_id,
          },
        };
        await this.$api.rejectFriend(params);
        this.$store.dispatch("removeFriendRequest", friend.user_id);
      } finally {
        this.loading = false;
      }
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
.request-item {
  width: auto;
  height: 100px;
  line-height: 50px;
  display: flex;
  align-items: center;
  flex-direction: column;
  border-bottom: solid 1px #eaecf1;
  .info {
    display: flex;
  }
}
.request-item:hover {
  background: #ececea;
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
  padding-left: 15px;
  font-size: 18px;
  color: rgb(84, 92, 100);
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  width: 200px;
}
.add {
  display: flex;
  justify-content: center;
  padding-bottom: 10px;
}
.search-result {
  padding-top: 50px;
  height: 200px;
  display: flex;
  justify-content: center;
  .item {
    width: 90%;
    display: flex;
    .left {
      width: 100px;
      border-right: solid 1px #eaecf1;
    }
    .right {
      width: 300px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      .result-name {
        font-size: 18px;
        color: rgb(84, 92, 100);
        font-weight: 600;
        height: 30px;
        line-height: 30px;
      }
      .result-des {
        height: 60px;
        line-height: 30px;
      }
    }
  }
}
</style>
