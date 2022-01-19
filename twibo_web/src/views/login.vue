<template>
  <div class="login-container">
    <transition name="el-zoom-in-center">
      <div class="login-form" v-show="show">
        <div class="head">
          <img src="../assets/avatar.jpg" alt="" />
        </div>
        <div class="logo">Welcome to Twibo!</div>
        <el-form
          :model="formData"
          label-position="right"
          label-width="50px"
          ref="formData"
          :rules="rules"
        >
          <el-form-item class="input-block" prop="email">
            <!-- <span slot="label" class="label">Account:</span> -->
            <el-input
              v-model="formData.email"
              placeholder="请输入账号"
              maxlength="50"
              @change="formData.email = formData.email.trim()"
            >
              <i slot="prefix" class="el-input__icon el-icon-user"></i>
            </el-input>
          </el-form-item>
          <el-form-item class="input-block" prop="password">
            <!-- <span slot="label" class="label">Password:</span> -->
            <el-input
              v-model="formData.password"
              maxlength="20"
              minlength="8"
              placeholder="请输入密码"
              @change="formData.password = formData.password.trim()"
              show-password
            >
              <i slot="prefix" class="el-input__icon el-icon-lock"></i>
            </el-input>
          </el-form-item>
          <div class="btn">
            <el-button
              type="primary"
              @click="login('formData')"
              native-type="submit"
              round
              >Login</el-button
            >
          </div>
        </el-form>

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
      rules: {
        email: [
          { required: true, message: "Email is required", trigger: "change" },
        ],
        password: [
          {
            required: true,
            message: "Password is required",
            trigger: "change",
          },
        ],
      },
      formData: {
        email: "",
        password: "",
      },
    };
  },
  mounted() {
    this.timer = setTimeout(() => (this.show = true), 300);
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  },
  methods: {
    async login(name) {
      this.$refs[name].validate((valid) => valid);
      if (!this.formData.email || !this.formData.password) {
        return;
      }
      const encryptPasswd = this.$getRsaCode(this.formData.password);

      const userInfo = await this.$api.login({
        email: this.formData.email,
        password: encryptPasswd,
      });
      this.$store.commit("login", userInfo);
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
  width: 320px;
  padding-left: 25px;
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
