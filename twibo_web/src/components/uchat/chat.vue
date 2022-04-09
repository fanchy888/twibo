<template>
  <el-card shadow="always" class="chat-block">
    <div class="chat-header">
      <span class="title">{{ chatInfo.name }}</span>
    </div>
    <div class="chat-content">
      <messageList></messageList>
    </div>
    <div class="chat-input">
      <el-input
        type="textarea"
        :rows="5"
        placeholder="说点什么吧"
        v-model="message"
        @keydown.enter.native="pressEnter($event)"
        :autofocus="true"
      >
      </el-input>
      <div class="btn">
        <el-button type="success" size="medium">发送</el-button>
      </div>
    </div>
  </el-card>
</template>
<script>
import messageList from "./message-list";
export default {
  name: "charRoom",
  components: { messageList },
  props: ["chatInfo"],
  data() {
    return {
      message: "",
    };
  },
  methods: {
    pressEnter(e) {
      e.preventDefault();
      if (e.shiftKey || e.ctrlKey) {
        this.message = this.message + "\n";
      } else {
        this.send();
      }
    },
    send() {
      this.message = "";
    },
  },
};
</script>
<style lang="scss" scoped>
.chat-block {
  height: 700px;
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
</style>
