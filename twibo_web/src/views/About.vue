<template>
  <div id="about">
    <h2>Vue.js WebSocket Tutorial</h2>
    <el-button @click="sendMessage('hello')">Send Message1</el-button>
    <el-button @click="getReply('hello')">twibo1</el-button>
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

  mounted() {
    this.$socket.open();
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
