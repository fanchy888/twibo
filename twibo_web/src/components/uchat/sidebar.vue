<template>
  <div class="side">
    <div class="search">
      <el-input
        prefix-icon="el-icon-search"
        v-model="searchInfo"
        placeholder="search"
      ></el-input>
    </div>
    <el-tabs v-model="activeName" type="border-card" stretch>
      <el-tab-pane name="chat">
        <span slot="label" style="font-size: 20px"
          ><el-badge is-dot :hidden="!unreadChat" style="line-height: 15px">
            <i class="el-icon-chat-line-round"></i></el-badge
        ></span>
        <div class="chat">
          <div
            v-for="(chat, index) in filterdChatList"
            :key="index.toString()"
            class="chat-item"
            @click="joinChat(chat)"
          >
            <el-badge is-dot style="height: 40px" :hidden="!checkUnread(chat)">
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
                <div class="msg">{{ getLastMsg(chat.messages) }}</div>
                <div class="time">{{ convertTime(chat.time) }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane name="friend">
        <span slot="label" style="font-size: 20px"
          ><el-badge
            is-dot
            :hidden="!friendRequests.length"
            style="line-height: 15px"
            ><i class="el-icon-user-solid"></i></el-badge
        ></span>
        <div class="chat" v-loading="loading">
          <div class="add">
            <el-button icon="el-icon-plus" @click="addVisible = true"
              >Add</el-button
            >
          </div>
          <el-collapse v-model="activeFriend">
            <el-collapse-item name="request" title="New Request">
              <template slot="title"
                >New Request
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
                    >Accept</el-button
                  >
                  <el-button
                    type="danger"
                    size="mini"
                    plain
                    @click="rejectFriend(friend)"
                    >Refuse</el-button
                  >
                </div>
              </div>
            </el-collapse-item>
            <el-collapse-item name="friend" title="Friends">
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
                  <el-popover
                    placement="right"
                    width="350"
                    :ref="`popRef${index}`"
                  >
                    <div class="pop-info" v-loading="editLoading">
                      <el-avatar
                        v-if="friend.avatar"
                        :src="avatarSrc(friend.avatar)"
                        :size="50"
                      ></el-avatar>
                      <el-avatar v-else :size="50">
                        <span style="font-size: 40px"
                          ><i class="el-icon-user"></i
                        ></span>
                      </el-avatar>
                      <div
                        style="
                          padding-top: 10px;
                          color: #a6a6a8;
                          font-size: 10px;
                        "
                      >
                        {{ friend.description }}
                      </div>
                      <div style="padding-top: 10px">
                        {{ friend.name }}
                      </div>
                      <div style="padding-top: 10px">
                        alias:
                        <el-input
                          size="small"
                          style="width: 100px"
                          v-model="friend.nick_name"
                          :disabled="!editName"
                          @blur="editFriend(friend)"
                        ></el-input
                        ><el-button
                          type=""
                          icon="el-icon-edit"
                          circle
                          size="mini"
                          @click="editName = true"
                          style="margin-left: 5px"
                        ></el-button>
                      </div>
                      <div style="padding-top: 50px">
                        <el-button
                          type="success"
                          size="small"
                          icon="el-icon-chat-dot-round"
                          @click="jumpToChat(friend, index)"
                          >Chat</el-button
                        >
                        <el-button
                          type="danger"
                          size="small"
                          icon="el-icon-delete"
                          @click="clickDelete(friend)"
                          >Delete</el-button
                        >
                      </div>
                    </div>

                    <el-button
                      slot="reference"
                      icon="el-icon-more"
                      circle
                      size="mini"
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
          placeholder="search"
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
        <div v-else>No Result</div>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex";
import { convertTime, avatarSrc } from "@/utils/common";

export default {
  name: "sideBar",
  props: ["friendList", "chatList", "friendRequests"],
  data() {
    return {
      activeName: "chat",
      activeFriend: ["friend"],
      searchInfo: "",
      addVisible: false,
      searchUserText: "",
      searchResult: null,
      dloading: false,
      loading: false,
      editLoading: false,
      editName: false,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
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
    unreadChat() {
      return this.chatList.filter((f) => this.checkUnread(f)).length;
    },
  },

  methods: {
    ...mapActions([
      "getUserInfo",
      "getChatList",
      "getFriends",
      "changeChatRoom",
    ]),
    avatarSrc: avatarSrc,
    convertTime: convertTime,

    joinChat(chat) {
      this.changeChatRoom(chat);
      this.$socket.emit("read", {
        user_id: this.user.user_id,
        chat_id: chat.chat_id,
      });
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
    async editFriend(friend) {
      this.editLoading = true;
      try {
        const params = {
          user_id: this.user.user_id,
          friend_user_id: friend.user_id,
          $body: friend,
        };
        await this.$api.updateFriend(params);
        await this.getChatList();
      } finally {
        this.editLoading = false;
        this.editName = false;
      }
    },
    jumpToChat(friend, index) {
      this.activeName = "chat";
      this.$refs["popRef" + index][0].doClose();
      const chat = this.chatList.find((c) => c.user_id === friend.user_id);
      if (chat) {
        this.joinChat(chat);
      }
    },

    async clickDelete(friend) {
      const res = await this.$confirm("Are you fucking sure?", {
        confirmButtonText: "FUCK YOU",
        cancelButtonText: "Just kidding",
        type: "warning",
      }).catch(() => {});
      if (res) {
        await this.deleteFriend(friend);
      }
    },

    async deleteFriend(friend) {
      this.editLoading = true;
      try {
        const param = {
          user_id: this.user.user_id,
          friend_user_id: friend.user_id,
        };
        await this.$api.deleteFriend(param);
        await this.getFriends();
        await this.getChatList();
      } finally {
        this.editLoading = false;
      }
    },

    getLastMsg(messages) {
      if (messages && messages.length > 0) {
        return messages[messages.length - 1].content;
      } else {
        return "";
      }
    },

    checkUnread(chat) {
      return (chat.messages || []).find(
        (m) => m.time >= chat.last_read && m.sender !== this.user.user_id
      );
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
    flex-direction: row;
    align-items: center;
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
    width: 110px;
  }
  .msg {
    font-size: 10px;
    width: 100px;
    color: #a6a6a8;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    text-align: left;
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
.pop-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: auto;
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
