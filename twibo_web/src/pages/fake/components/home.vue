<template>
  <div>
    <transition name="el-fade-in-linear">
      <jump v-show="showFlag === 1" @cancelJump="showFlag = 0"></jump>
    </transition>
    <transition name="el-fade-in-linear">
      <trick
        v-show="showFlag === 2"
        @cancelJump="showFlag = 0"
        :lines="trickLines"
      ></trick>
    </transition>
    <transition name="el-zoom-in-center">
      <gallery
        v-show="showFlag == 0"
        @showJump="showJump"
        @showTrick="showTrick"
      ></gallery
    ></transition>
  </div>
</template>
<script>
import jump from "./jump";
import trick from "./trick";
import gallery from "./gallery";
export default {
  components: { jump, gallery, trick },
  data() {
    return {
      showFlag: 0,
      trickLines: "Less is More",
    };
  },
  methods: {
    showJump() {
      this.showFlag = 1;
    },
    showTrick(line) {
      this.showFlag = 2;
      this.trickLines = line;
    },
  },
};
</script>
<style scoped lang="scss">
.el-fade-in-linear-enter-active,
.el-fade-in-linear-leave-active {
  transition: opacity 3s;
}
.el-fade-in-linear-enter, .el-fade-in-linear-leave /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
