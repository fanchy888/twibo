<template>
  <div class="home">
    <el-button type="primary" @click="test">fuck you</el-button>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {},
  methods: {
    test() {
      console.log("===fuck you");
      this.$api.getUserInfo();
    },
  },
};
</script>
