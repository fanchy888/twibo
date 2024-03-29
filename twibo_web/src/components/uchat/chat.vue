<template>
  <el-card shadow="always" class="chat-block">
    <div class="chat-header">
      <span class="title">{{ chatInfo.name }}</span>
    </div>
    <div class="chat-content" id="content">
      <messageList ref="messageList"></messageList>
    </div>
    <div class="chat-input">
      <div class="chat-tool">
        <emoji @emoji_click="selectEmoji"></emoji>
        <uploadImg
          :chatInfo="chatInfo"
          @updateLastRead="updateLastRead"
        ></uploadImg>
      </div>
      <el-input
        type="textarea"
        :rows="5"
        placeholder="Say something..."
        v-model="message"
        @keydown.enter.native="pressEnter($event)"
        :autofocus="true"
        resize="none"
      >
      </el-input>
      <div class="btn">
        <el-button
          :disabled="!message"
          type="success"
          size="medium"
          @click="send"
          >Send</el-button
        >
      </div>
    </div>
  </el-card>
</template>
<script>
import messageList from "./message-list";
import { mapActions, mapState } from "vuex";
import emoji from "./emoji";
import uploadImg from "./file-upload/img";
export default {
  name: "chatRoom",
  components: { messageList, emoji, uploadImg },
  props: ["chatInfo"],
  watch: {
    chatInfo() {
      this.$refs.messageList.scrollToBottom();
    },
  },
  data() {
    return {
      message: "",
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
  },
  mounted() {
    document.addEventListener("click", this.onClick);
  },
  beforeDestroy() {
    document.removeEventListener("click", this.onClick);
  },
  methods: {
    ...mapActions(["updateLastRead"]),
    pressEnter(e) {
      e.preventDefault();
      if (e.shiftKey || e.ctrlKey) {
        this.message = this.message + "\n";
      } else {
        this.send();
      }
    },
    send() {
      if (!this.message) {
        return;
      }
      const msg = {
        content: this.message,
        chat_id: this.chatInfo.chat_id,
        sender: this.user.user_id,
      };
      this.updateLastRead();
      this.$socket.emit("read", {
        user_id: this.user.user_id,
        chat_id: msg.chat_id,
      });
      this.$socket.emit("chat", msg);
      this.message = "";
    },
    onClick(e) {
      if (document.getElementById("content").contains(e.target)) {
        this.updateLastRead();
        this.$socket.emit("read", {
          user_id: this.user.user_id,
          chat_id: this.chatInfo.chat_id,
        });
      }
    },
    selectEmoji(emoji) {
      this.message = this.message + emoji;
    },
  },
};
</script>
<style lang="scss" scoped>
.chat-block {
  height: 750px;
}
.chat-header {
  height: 40px;
  line-height: 40px;

  .title {
    font-size: 25px;
    font-weight: bold;
    color: #545c64;
  }
}
.chat-content {
  height: 450px;
  border: 1px solid #eaecf1;
}
.chat-input {
  height: 150px;
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  .btn {
    padding-top: 5px;
    height: 40px;
    line-height: 40px;
    text-align: right;
  }
}
.chat-tool {
  display: flex;
  height: 20px;
  line-height: 20px;
  margin-bottom: 5px;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
</style>
