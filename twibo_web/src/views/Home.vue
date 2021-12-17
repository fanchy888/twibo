<template>
  <div class="home">
    <el-button type="primary" @click="test">Test</el-button>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {},
  methods: {
    test() {
      console.log("click");
      this.$api.getUserInfo({ $query: { uid: 123 } });
    },
  },
};
</script>
