<template>
  <div class="msg">
    <div
      v-for="(msg, index) in msgList"
      :key="index"
      class="msg-item"
      :style="
        msg.sender === user.user_id ? { 'flex-direction': 'row-reverse' } : {}
      "
    >
      <span>{{ msg.sender }}</span>

      <span>{{ msg.msg }}</span>
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";

export default {
  name: "messageList",
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
  },

  data() {
    return {
      msgList: [
        { sender: "user-MjExMjI1MjE0MzI5", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
        { sender: "123", msg: "hi" },
      ],
    };
  },
};
</script>
<style lang="scss" scoped>
.msg {
  height: 450px;
  overflow-y: auto;
}
.msg-item {
  display: flex;
  height: 50px;
  line-height: 50px;
}
</style>
