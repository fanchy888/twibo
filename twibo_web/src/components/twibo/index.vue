<template>
  <el-card shadow="always" style="height: 100%">
    <el-container class="twibo">
      <el-main>
        <el-empty
          :image-size="200"
          description="Twitter is not Weibo"
        ></el-empty>
        <TwiboEditor></TwiboEditor>
      </el-main>
    </el-container>
  </el-card>
</template>
<script>
import TwiboEditor from "./editor";
export default {
  name: "Twibo",
  components: { TwiboEditor },
};
</script>
<style lang="scss" scoped></style>
