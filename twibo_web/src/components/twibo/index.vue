<template>
  <el-card shadow="always" style="height: 100%">
    <el-container class="twibo">
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-card>
</template>
<script>
export default {
  name: "Twibo",
  methods: {},
};
</script>
<style lang="scss" scoped></style>
