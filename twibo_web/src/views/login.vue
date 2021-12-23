<template>
  <div class="login-container">
    <transition name="el-zoom-in-center">
      <div class="login-form" v-show="show">
        <div class="head">
          <img src="../assets/avatar.jpg" alt="" />
        </div>
        <div class="logo">Welcome to Twibo!</div>
        <el-form v-model="formData" label-position="right" label-width="80px">
          <el-form-item class="input-block">
            <span slot="label" class="label">E-mail:</span>
            <el-input
              v-model="formData.email"
              placeholder=""
              maxlength="50"
            ></el-input>
          </el-form-item>
          <el-form-item class="input-block">
            <span slot="label" class="label">Password:</span>
            <el-input
              v-model="formData.password"
              maxlength="20"
              minlength="8"
              show-word-limit
              show-password
            ></el-input>
          </el-form-item>
        </el-form>
        <div class="btn">
          <el-button type="primary" @click="login" round>Login</el-button>
        </div>
        <div class="foot">
          Don't hava an account?
          <span class="foot-btn" @click="register">Register Now</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "login",
  components: {},
  data() {
    return {
      show: false,
      timer: "",
      formData: {
        email: "",
        password: "",
      },
    };
  },
  mounted() {
    this.timer = setTimeout(() => (this.show = true), 500);
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  },
  methods: {
    login() {
      console.log("login", this.formData);
      const encryptPasswd = this.$getRsaCode(this.formData.password);
      console.log(encryptPasswd);
      // await this.$api.login();
      this.$api.getUserInfo({ $query: { user_id: "user-MjExMjI0MDA0NjE5" } });
      const token = "123";
      this.$store.commit("login", token);
      let redirect = decodeURIComponent(this.$route.query.redirect || "/");
      this.$router.push(redirect);
    },
    register() {
      this.$router.push("/register");
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
  margin-bottom: 30px;
  height: 50px;
}
.input-block {
  width: 330px;
  padding-left: 40px;
  font-size: 15px;
  font-weight: 600;
  color: #8696a7;
}
.btn {
  position: relative;
  text-align: center;
  margin-top: 40px;
  margin-bottom: 10px;
}
.foot {
  font-size: 13px;
  color: #bfbfbf;
  text-align: center;
}
.foot-btn {
  color: #409eff;
  font-size: 13px;
}
.foot-btn:hover {
  color: #e6a23c;
  cursor: pointer;
}
</style>
