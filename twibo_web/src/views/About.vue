<template>
  <div id="about">
    <h2>Vue.js WebSocket Tutorial</h2>
    <el-button @click="sendMessage('hello')">Send Message</el-button>
    <el-button @click="getReply('hello')">twibo</el-button>
    <span>{{ message }}</span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "",
    };
  },
  sockets: {
    connect() {
      console.log("链接成功");
    },
    disconnect() {
      console.log("断开链接");
    }, //检测socket断开链接
    reconnect() {
      console.log("重新链接");
    },
    //客户端接收后台传输的socket事件
    message(data) {
      this.$notify({
        title: "新消息",
        message: data,
        type: "warning",
        duration: 10000,
      });
      this.message = data;
      console.log("data", data); //接收的消息
    },
    received(res) {
      console.log(res);
    },
  },

  mounted() {
    this.$socket.emit("connect1"); // 在页面加载时发起订阅，“STREAM_STATUS”是你跟后端约定好的主题名
  },
  methods: {
    sendMessage(data) {
      this.$socket.emit("message", data);
    },
    getReply(data) {
      this.$socket.emit("auto_reply", data);
    },
  },
};
</script>
