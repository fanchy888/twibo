<template>
  <el-header><span class="logo">Twibo</span></el-header>
</template>
<script>
export default {
  name: "mainHeader",
};
</script>
<style lang="scss" scoped>
.el-header {
  background-color: #2c3e50;
  text-align: center;
  height: 80px;
  line-height: 80px;
}
.logo {
  color: #ececea;
  font-family: "PingFang SC";
  font-size: 30px;
  font-weight: 600;
  text-shadow: -4px 6px 3px #060606;
}
</style>
