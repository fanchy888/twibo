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
  name: "home",
  data() {
    return {
      message: "",
    };
  },
  mounted() {
    if (!this.$store.state.Socket.isConnected) {
      this.$socket.open();
    }
    this.sockets.subscribe("message", (data) => {
      console.log(data);
    });
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
