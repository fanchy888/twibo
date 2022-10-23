<template>
  <div class="top">
    <div @click="cancel" class="title">
      <span class="info" tabindex="1">{{ lines }}</span>
    </div>
    <transition name="el-fade-in-linear">
      <div v-if="pill" class="card"></div>
    </transition>
  </div>
</template>
<script>
export default {
  name: "trick",
  props: ["lines"],
  data() {
    return {
      pill: false,
    };
  },
  methods: {
    cancel() {
      this.pill = false;
      this.$emit("cancelJump");
    },
  },
};
</script>
<style lang="scss" scoped>
.top {
  position: absolute;

  background-color: #ffffff;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.title {
  height: 40%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.info {
  color: #222222;
  font-size: 30px;
  box-sizing: border-box;
  width: 800px;
  height: 50px;
  display: flex;
  align-content: center;
  justify-content: center;
  align-items: center;
}

.info:hover {
  cursor: pointer;
  transition: 3s linear;
}

.info:focus {
  color: #05dd29;
}
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 30px;
  color: #222222;
}
.el-fade-in-linear-enter-active {
  transition: opacity 3s;
}
.el-fade-in-linear-enter/* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
