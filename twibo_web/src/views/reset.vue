<template>
  <div class="login-container">
    <transition name="el-zoom-in-center">
      <div class="login-form" v-show="show" v-loading="loading">
        <div class="head">
          <img src="../assets/avatar.jpg" alt="" />
        </div>
        <div class="logo">Reset Password</div>
        <el-form
          :model="formData"
          ref="formData"
          status-icon
          :rules="rules"
          label-position="left"
        >
          <el-form-item class="input-block" prop="account">
            <span slot="label" class="label">Acount:</span>
            <el-input
              v-model="formData.account"
              placeholder=""
              maxlength="50"
              @change="formData.account = formData.account.trim()"
            ></el-input>
          </el-form-item>
          <el-form-item class="input-block" prop="email">
            <span slot="label" class="label">E-mail:</span>
            <el-input
              v-model="formData.email"
              placeholder=""
              @change="formData.email = formData.email.trim()"
            ></el-input>
          </el-form-item>

          <!-- <el-form-item class="input-block" prop="password">
            <span slot="label" class="label">Password:</span>
            <el-input
              v-model="formData.password"
              maxlength="20"
              minlength="8"
              show-password
              placeholder="8 ~ 20 characters"
              required
              @change="formData.password = formData.password.trim()"
            ></el-input>
          </el-form-item>
          <el-form-item class="input-block" prop="confirmPassword">
            <span slot="label" class="label">Confirm Password:</span>
            <el-input
              v-model="formData.confirmPassword"
              maxlength="20"
              minlength="8"
              placeholder="8 ~ 20 characters"
              @change="
                formData.confirmPassowrd = formData.confirmPassword.trim()
              "
              show-password
            ></el-input>
          </el-form-item> -->
        </el-form>
        <div class="info">
          Enter your account as well as the binded email address. A randomly
          generated password will be set to your account.
        </div>
        <div label="" class="btn">
          <el-button
            type="success"
            @click="submit('formData')"
            round
            :disabled="disabled"
          >
            {{ btnText }}
          </el-button>
        </div>
        <div class="foot">
          <span class="foot-btn" @click="login">Jump to Login Page</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "reset",
  components: {},
  data() {
    return {
      timer: null,
      interval: null,
      show: false,
      disabled: false,
      totalCount: 60,
      rules: {
        account: [
          { required: true, message: "account is required", trigger: "change" },
        ],
        email: [
          { required: true, message: "E-mail is required", trigger: "change" },
        ],
      },
      loading: false,
      formData: {
        account: "",
      },
    };
  },
  computed: {
    btnText() {
      return this.totalCount !== 0 && this.disabled
        ? `Reset(${this.totalCount}s)`
        : "Reset";
    },
  },

  mounted() {
    this.timer = setTimeout(() => (this.show = true), 300);
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  },
  methods: {
    async submit(name) {
      this.$refs[name].validate((valid) => valid);
      if (!this.formData.email || !this.formData.account) {
        return;
      }
      const param = {
        $body: {
          account: this.formData.account,
          email: this.formData.email,
        },
      };
      this.loading = true;
      try {
        const user = await this.$api.resetPassword(param);
        if (user) {
          this.$message({
            type: "success",
            message:
              "A New password has been sent to your email address, please check it soon.",
            duration: 5000,
          });
          this.disabled = true;

          this.interval = setInterval(() => {
            this.totalCount--;
            if (this.totalCount === 0) {
              clearInterval(this.interval);
              this.disabled = false;
              this.totalCount = 60;
            }
          }, 1000);
          //   this.$router.push("/login");
        }
      } finally {
        this.loading = false;
      }
    },
    login() {
      if (!localStorage.token) {
        this.$router.push("/login");
      } else {
        this.$router.push("/");
      }
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
  height: 600px;
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
  margin-top: -60px;
  margin-bottom: 20px;
  height: 50px;
}
.input-block {
  width: 330px;
  height: 60px;
  font-size: 13px;
  font-weight: 600;
  color: #8696a7;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 25px;
}
.btn {
  position: relative;
  text-align: center;
  margin-top: 40px;
  margin-bottom: 10px;
}
.info {
  font-size: 13px;
  color: #bfbfbf;
  text-align: left;
  padding-left: 30px;
  padding-right: 30px;
  padding-top: 20px;
}
.foot {
  font-size: 13px;
  color: #bfbfbf;
  text-align: center;
}
.foot-btn {
  color: #bfbfbf;
  font-size: 13px;
}
.foot-btn:hover {
  color: #e6a23c;
  cursor: pointer;
}
</style>
