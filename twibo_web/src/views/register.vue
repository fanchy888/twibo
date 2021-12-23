<template>
  <div class="login-container">
    <transition name="el-zoom-in-center">
      <div class="login-form">
        <div class="head">
          <img src="../assets/avatar.jpg" alt="" />
        </div>
        <div class="logo">Join Twibo Now!</div>
        <el-form>
          <el-form-item label="" class="btn">
            <el-button type="primary" size="medium" @click="submit">
              Submit
            </el-button>
          </el-form-item>
        </el-form>
        Already has an account? Try login
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "register",
  components: {},
  data() {
    return {};
  },

  beforeDestroy() {
    clearTimeout(this.timer);
  },
  methods: {
    async submit() {
      console.log("submmit");
      const param = {
        $body: {
          name: "root",
          password: this.$getRsaCode("123456"),
          email: "123@qq.com",
        },
      };
      const user = await this.$api.register(param);
      console.log(user);
    },
  },
};
</script>

<style lang="scss" scoped>
.login-container {
  background-color: #2c3e50;
  height: 100%;
  width: 100%;
}
.login-form {
  width: 400px;
  height: 500px;
  top: 50%;
  left: 50%;
  border: 2px solid #eee;
  border-radius: 13px;
  background-color: aliceblue;
  position: absolute;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px #ddd;
}
.head {
  height: 200px;
  width: 200px;
  border: 5px solid #eee;
  border-radius: 50%;
  box-shadow: 0 0 10px #ddd;
  position: relative;
  left: 50%;
  transform: translate(-50%, -50%);
}
img {
  height: 100%;
  width: 100%;
  border-radius: 50%;
  background-color: #eee;
}
.logo {
  font-size: 25px;
  font-weight: 600;
  text-shadow: 2px 2px 2px #ddd;
  color: #8696a7;
  text-align: center;
  position: relative;
  margin-top: -40px;
  margin-bottom: 50px;
  height: 50px;
}
.btn {
  position: relative;
  text-align: center;
}
</style>
