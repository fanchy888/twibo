<template>
  <div class="top">
    <div @click="pill = true" class="title">
      <span class="info" tabindex="1"
        >You ever have that feeling where you're not sure if you're awake or
        still dreaming?</span
      >
    </div>
    <transition name="el-fade-in-linear">
      <div v-if="pill" class="card">
        <div>Ready to take pills?</div>
        <div>
          <el-button type="danger" @click="jump2twibo" round></el-button>
          <el-button type="primary" @click="cancel" round></el-button>
        </div>
      </div>
    </transition>
  </div>
</template>
<script>
export default {
  name: "jump",
  data() {
    return {
      pill: false,
    };
  },
  methods: {
    jump2twibo() {
      this.$cookies.set("safeword", "lessismore", -1);
      this.$router.replace("/twibo");
      location.reload();
    },
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

  background-color: #020303;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.curser {
  position: absolute;
  left: 0;
  top: 0;
  color: #05dd29;
}
.title {
  height: 40%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.info {
  color: transparent;
  font-size: 30px;
  box-sizing: border-box;
  text-shadow: 0px 2px 12px #05921d;
  width: 800px;
  height: 50px;
  display: flex;
  align-content: center;
  justify-content: center;
  align-items: center;
}

.info:hover {
  color: #09b325;
  cursor: pointer;
  transition: 3s linear;
}

.info:focus {
  color: #09b325;
  text-shadow: 0px 5px 5px #05921d;
}
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 30px;
  color: #05dd29;
}
.el-fade-in-linear-enter-active,
.el-fade-in-linear-leave-active {
  transition: opacity 5s;
}
.el-fade-in-linear-enter, .el-fade-in-linear-leave /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
