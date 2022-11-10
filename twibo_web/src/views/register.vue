<template>
  <div class="login-container">
    <transition name="el-zoom-in-center">
      <div class="login-form" v-show="show" v-loading="loading">
        <div class="head">
          <img src="../assets/avatar.jpg" alt="" />
        </div>
        <div class="logo">Join Twibo Now!</div>
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
              maxlength="50"
              @change="formData.email = formData.email.trim()"
            ></el-input>
          </el-form-item>
          <el-form-item class="input-block" prop="name">
            <span slot="label" class="label">Name:</span>
            <el-input
              v-model="formData.name"
              placeholder=""
              maxlength="50"
              show-word-limit
              @change="formData.name = formData.name.trim()"
            ></el-input>
          </el-form-item>

          <el-form-item class="input-block" prop="password">
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
          </el-form-item>
        </el-form>
        <div label="" class="btn">
          <el-button type="success" @click="submit('formData')" round>
            Register
          </el-button>
        </div>
        <div class="foot">
          Already has an account?
          <span class="foot-btn" @click="login">Login</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "register",
  components: {},
  data() {
    var validPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error("Password is required"));
      } else if (this.formData.confirmPassword) {
        this.$refs.formData.validateField("confirmPassword");
      }
      callback();
    };

    var checkPassword = (rule, value, callback) => {
      if (value !== this.formData.password) {
        callback(new Error("Password inconsistent"));
      }
      callback();
    };
    return {
      timer: null,
      show: false,
      rules: {
        name: [
          { required: true, message: "Name is required", trigger: "change" },
        ],
        email: [
          { required: true, message: "Email is required", trigger: "change" },
        ],
        account: [
          { required: true, message: "Account is required", trigger: "change" },
        ],
        password: [
          { validator: validPassword, trigger: "change" },
          {
            required: true,
            message: "Password is required",
            trigger: "change",
          },
          {
            min: 8,
            max: 20,
            message: "Password must be 8 to 20 characters",
            trigger: "blur",
          },
        ],
        confirmPassword: [
          { validator: checkPassword, trigger: "change" },
          {
            required: true,
            message: "Password inconsistent",
            trigger: "change",
          },
          {
            min: 8,
            max: 20,
            message: "Password must be 8 to 20 characters",
            trigger: "change",
          },
        ],
      },
      loading: false,
      formData: {
        name: "",
        account: "",
        email: "",
        password: "",
        confirmPassword: "",
        inviteCode: "",
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
    async submit(name) {
      this.$refs[name].validate((valid) => valid);
      if (
        !this.formData.account ||
        !this.formData.email ||
        !this.formData.password ||
        !this.formData.confirmPassword ||
        !this.formData.name ||
        this.formData.confirmPassword !== this.formData.password
      ) {
        return;
      }
      const param = {
        $body: {
          name: this.formData.name,
          password: this.$getRsaCode(this.formData.password),
          email: this.formData.email,
          account: this.formData.account,
        },
      };
      this.loading = true;
      try {
        const user = await this.$api.register(param);
        if (user) {
          this.$message({
            type: "success",
            message: "Create successfully! Welcome!",
            duration: 2000,
          });
          this.$router.push("/login");
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
  height: 730px;
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
  margin-top: -80px;
  height: 50px;
}
.input-block {
  width: 330px;
  height: 70px;
  font-size: 13px;
  font-weight: 600;
  color: #8696a7;
  margin-left: auto;
  margin-right: auto;
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
  font-size: 14px;
}
.foot-btn:hover {
  color: #e6a23c;
  cursor: pointer;
}
</style>
