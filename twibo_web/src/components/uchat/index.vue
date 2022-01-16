<template>
  <el-card shadow="always" style="height: 100%">
    <el-container class="uchat">
      <el-aside width="300px">
        <sideBar></sideBar>
      </el-aside>
      <el-container>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </el-card>
</template>
<script>
import sideBar from "./sidebar";

export default {
  components: { sideBar },
  name: "youChat",
  data() {
    return {
      friends: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4,
        4,
      ],
    };
  },
};
</script>
<style lang="scss" scoped>
.uchat {
  height: 600px;
}
</style>
