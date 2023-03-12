<template>
  <div class="card">
    <el-card>{{ task.title }} </el-card>
  </div>
</template>
<script>
export default {
  name: "taskItem",
  props: ["task"],
};
</script>
<style lang="scss" scoped>
.card {
  padding: 10px;
}
</style>
