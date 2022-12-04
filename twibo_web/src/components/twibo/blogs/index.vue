<template>
  <div class="blog">
    <el-empty :image-size="200" description="Twitter is not Weibo"></el-empty>
    <el-button @click="edit">Create</el-button>
  </div>
</template>
<script>
export default {
  name: "Blog",
  methods: {
    edit() {
      this.$router.push({ name: "edit" });
    },
  },
};
</script>
<style lang="scss" scoped>
.blog {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
