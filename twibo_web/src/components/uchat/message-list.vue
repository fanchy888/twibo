<template>
  <div class="msg" id="scroll">
    <div v-for="(msg, index) in messages" :key="index" class="msg-item">
      <div v-if="msg.sender === user.user_id" class="right">
        <div class="info">
          <div class="content">
            <div class="detail">
              {{ msg.content }}
            </div>
            <div class="time">
              {{ convertTime(msg.time) }}
            </div>
          </div>
        </div>
        <el-avatar
          v-if="msg.avatar"
          :src="avatarSrc(msg.avatar)"
          :size="40"
          shape="square"
        ></el-avatar>
        <el-avatar v-else :size="40" shape="square">
          <span style="font-size: 30px"><i class="el-icon-user"></i></span>
        </el-avatar>
      </div>
      <div v-else class="left">
        <el-avatar
          v-if="msg.avatar"
          :src="avatarSrc(msg.avatar)"
          :size="40"
          shape="square"
        ></el-avatar>
        <el-avatar v-else :size="40" shape="square">
          <span style="font-size: 30px"><i class="el-icon-user"></i></span>
        </el-avatar>
        <div class="info">
          <div class="title">{{ msg.name }}</div>
          <div class="content">
            <div class="detail">
              {{ msg.content }}
            </div>
            <div class="time">
              {{ convertTime(msg.time) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";
import { avatarSrc, timedelta } from "@/utils/common";
export default {
  name: "messageList",
  props: [],
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendList: (state) => state.Friend.friendList,
      chatList: (state) => state.Chat.chatList,
      currentChat: (state) => state.Chat.currentChat,
    }),

    messages() {
      const msgs = this.currentChat.messages;
      const members = this.currentChat.members;
      msgs.map((m) => {
        let sender =
          members.find((member) => member.user_id === m.sender) || {};
        m.avatar = sender.avatar;
        m.name = sender.name;
      });
      return msgs;
    },
  },
  watch: {
    messages() {
      this.scrollToBottom();
    },
  },
  mounted() {
    this.scrollToBottom();
  },
  data() {
    return {};
  },
  methods: {
    avatarSrc: avatarSrc,
    scrollToBottom() {
      this.$nextTick(() => {
        var container = document.getElementById("scroll");
        container.scrollTop = container.scrollHeight;
      });
    },
    convertTime(t) {
      if (!t) return "";
      const time = new Date(t * 1000 - timedelta);
      const year = time.getFullYear();
      const month = time.getMonth() + 1;
      const day = time.getDate();
      const hour = time.getHours();
      let minite = time.getMinutes();
      if (minite < 10) {
        minite = "0" + minite;
      }
      return year + "-" + month + "-" + day + " " + hour + ":" + minite;
    },
  },
};
</script>
<style lang="scss" scoped>
.msg {
  height: 450px;
  overflow-y: auto;
}
.msg-item {
  .left {
    display: flex;
    max-width: 50%;
    text-align: left;
    padding-left: 20px;
    .info {
      .title {
        line-height: 10px;
        font-size: 13px;
        color: #45494d;
        font-weight: 300;
        padding-left: 10px;
      }
      .content {
        padding-left: 10px;
        display: inline-block;
        .time {
          line-height: 10px;
          font-size: 12px;
          color: #a6a6a8;
        }
        .detail {
          font-size: 15px;
          font-weight: 600;
          color: #4c4c4c;
          margin-top: 5px;
          background: #dbdbdb;
          border-radius: 20px;
          word-break: break-all;
          word-wrap: break-word;
          text-align: left;
          line-height: 20px;
          padding-inline: 20px;
          padding-top: 10px;
          padding-bottom: 10px;
          white-space: pre-line;
          max-width: 400px;
        }
      }
    }
  }
  .right {
    position: relative;
    max-width: 50%;
    left: 50%;
    display: flex;
    justify-content: flex-end;
    text-align: right;
    padding-right: 20px;
    .info {
      text-align: right;

      .title {
        line-height: 10px;
        font-size: 15px;
        color: #2c3e50;
        font-weight: 300;
        padding-right: 10px;
      }
      .content {
        padding-right: 10px;
        display: inline-block;
        .time {
          line-height: 10px;
          font-size: 12px;
          color: #a6a6a8;
        }
        .detail {
          font-size: 15px;
          font-weight: 600;
          color: #4c4c4c;
          margin-top: 5px;
          background: #a3c3f6;
          border-radius: 20px;
          word-break: break-all;
          word-wrap: break-word;
          text-align: left;
          line-height: 20px;
          padding-inline: 20px;
          padding-top: 10px;
          padding-bottom: 10px;
          white-space: pre-line;
          max-width: 400px;
        }
      }
    }
  }
  min-height: 50px;
  line-height: 50px;
}
</style>
