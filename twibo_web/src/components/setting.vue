<template>
  <el-card shadow="always" style="height: 100%">
    <div class="main-avatar">
      <el-upload
        action="a"
        :http-request="uploadAvatar"
        :before-upload="beforeUpload"
        :show-file-list="false"
      >
        <div slot="trigger" class="upload">
          <el-tooltip effect="dark" :content="tooltipInfo" placement="top">
            <el-avatar
              v-loading="loading"
              v-if="user && user.avatar"
              :size="100"
              :src="avatarSrc(user.avatar)"
              fit="contain"
              class="ava-child"
            ></el-avatar>
            <el-avatar v-else :size="100" class="ava-child">
              <span style="font-size: 50px"><i class="el-icon-user"></i></span>
            </el-avatar>
          </el-tooltip>
        </div>
      </el-upload>
    </div>
    <el-form
      v-loading="loading"
      :model="userForm"
      ref="formData"
      label-width="100px"
      label-position="right"
      class="user-form"
    >
      <el-form-item label="account:">
        <el-input v-model="userForm.account" disabled></el-input>
      </el-form-item>
      <el-form-item label="name:">
        <el-input
          v-model="userForm.name"
          maxlength="20"
          show-word-limit
          @change="userForm.name = userForm.name.trim()"
        ></el-input>
      </el-form-item>
      <el-form-item label="description:">
        <el-input
          v-model="userForm.description"
          maxlength="50"
          show-word-limit
          autosize
          @change="userForm.description = userForm.description.trim()"
          type="textarea"
        ></el-input>
      </el-form-item>

      <el-form-item label="E-mail:">
        <el-input v-model="userForm.email"></el-input>
      </el-form-item>
    </el-form>
    <div class="foot">
      <el-button @click="updateInfo" type="primary" round plain class="btn"
        >Save</el-button
      >
      <span class="foot-btn" @click="passwordVisible = true"
        >Change Password</span
      >
    </div>

    <el-dialog
      :visible.sync="passwordVisible"
      center
      width="550px"
      class="my-dialog"
      title="Change Password"
    >
      <el-form
        v-loading="dloading"
        :model="passwordForm"
        ref="pswdData"
        label-width="200px"
        label-position="right"
        class="pwd-form"
        :rules="rules"
      >
        <el-form-item class="input-block" label="Old Password:" prop="old">
          <el-input
            v-model="passwordForm.old"
            maxlength="20"
            minlength="8"
            show-password
            placeholder="8 ~ 20 characters"
            required
            @change="passwordForm.old = passwordForm.old.trim()"
          ></el-input>
        </el-form-item>
        <el-form-item class="input-block" label="New Password:" prop="new">
          <el-input
            v-model="passwordForm.new"
            maxlength="20"
            minlength="8"
            show-password
            placeholder="8 ~ 20 characters"
            required
            @change="passwordForm.new = passwordForm.new.trim()"
          ></el-input>
        </el-form-item>
        <el-form-item
          class="input-block"
          label="Confirm Password:"
          prop="repeat"
        >
          <el-input
            v-model="passwordForm.repeat"
            maxlength="20"
            minlength="8"
            show-password
            placeholder="8 ~ 20 characters"
            required
            @change="passwordForm.repeat = passwordForm.repeat.trim()"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button type="primary" @click="changePassword()">Confirm</el-button>
      </span>
    </el-dialog>
  </el-card>
</template>
<script>
import { mapActions, mapState } from "vuex";
import { avatarSrc } from "@/utils/common";

export default {
  name: "setting",
  data() {
    var validPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error("Password is required"));
      } else if (this.passwordForm.repeat) {
        this.$refs.pswdData.validateField("repeat");
      }
      callback();
    };

    var checkPassword = (rule, value, callback) => {
      if (value !== this.passwordForm.new) {
        callback(new Error("Password inconsistent"));
      }
      callback();
    };
    return {
      loading: false,
      dloading: false,
      passwordVisible: false,
      userForm: { name: "", description: "", account: "", email: "" },
      passwordForm: { old: "", new: "", repeat: "" },
      rules: {
        old: [
          {
            required: true,
            message: "Old password is required",
            trigger: "change",
          },
          {
            min: 8,
            max: 20,
            message: "Password must be 8 to 20 characters",
            trigger: "blur",
          },
        ],
        new: [
          { validator: validPassword, trigger: "change" },
          {
            required: true,
            message: "New password is required",
            trigger: "change",
          },
          {
            min: 8,
            max: 20,
            message: "Password must be 8 to 20 characters",
            trigger: "change",
          },
        ],
        repeat: [
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
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),

    tooltipInfo() {
      return this.user && this.user.avatar ? "点击修改头像" : "上传头像";
    },
  },
  async mounted() {
    if (!this.user) {
      await this.getUserInfo();
    }
    this.userForm.name = this.user.name;
    this.userForm.description = this.user.description;
    this.userForm.account = this.user.account;
    this.userForm.email = this.user.email;
  },
  methods: {
    ...mapActions(["getUserInfo"]),
    avatarSrc: avatarSrc,

    async uploadAvatar(param) {
      let data = new FormData();
      data.append("file", param.file);
      data.append("type", "avatar");
      data.append("user_id", this.user.user_id);
      try {
        this.loading = true;
        const res = await this.$api.upload({ $body: data });
        if (res.success) {
          this.$message({
            type: "success",
            message: "上传成功",
            duration: 2000,
          });
        }
        await this.getUserInfo();
      } finally {
        this.loading = false;
      }
    },
    beforeUpload(file) {
      const isValidType = ["image/jpeg", "image/png", "image/gif"].includes(
        file.type
      );
      const isValidSize = file.size / 1024 < 500;
      if (!isValidType) {
        this.$message.error("请上传png/jpg/jpeg/gif格式的图片");
      }
      if (!isValidSize) {
        this.$message.error("文件大小不超过500kb");
      }
      return isValidSize && isValidType;
    },
    async updateInfo() {
      this.loading = true;
      try {
        const param = {
          $query: {
            user_id: this.user.user_id,
          },
          $body: this.userForm,
        };
        const res = await this.$api.updateUserInfo(param);
        await this.getUserInfo();
        if (res.success) {
          this.$message({
            message: "更新成功",
            type: "success",
          });
        }
      } finally {
        this.loading = false;
      }
    },
    clearPwdForm() {
      this.passwordForm.old = "";
      this.passwordForm.new = "";
      this.passwordForm.repeat = "";
    },
    async changePassword() {
      this.$refs.pswdData.validate((valid) => valid);
      if (
        !this.passwordForm.new ||
        !this.passwordForm.old ||
        !this.passwordForm.repeat ||
        this.passwordForm.repeat !== this.passwordForm.new
      ) {
        return;
      }
      this.dloading = true;

      try {
        const param = {
          user_id: this.user.user_id,

          $body: {
            new: this.$getRsaCode(this.passwordForm.new),
            old: this.$getRsaCode(this.passwordForm.old),
          },
        };

        const res = await this.$api.changePassword(param);
        if (res.success) {
          this.$message({
            message: "密码更新成功",
            type: "success",
          });
          this.passwordVisible = false;
        }
      } finally {
        this.dloading = false;
        this.$refs.pswdData.resetFields();
        // this.clearPwdForm();
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.main-avatar {
  height: 100px;
  width: 100px;
  margin: auto;
  margin-top: 50px;
  display: flex;
  align-content: center;
  justify-content: center;
  align-items: flex-start;
}
.upload {
  height: 100px;
  & :hover {
    box-shadow: 0 0 10px #666;
  }
  .ava-child :hover {
    box-shadow: unset;
  }
}
.user-form {
  width: 400px;
  margin-left: 35%;
  margin-top: 50px;
  line-height: 50px;
}
.btn {
  padding-top: 10px;
}

.foot {
  color: #bfbfbf;
  padding-top: 10px;
  display: flex;
  flex-direction: column;

  align-items: center;
  line-height: 20px;
}
.foot-btn {
  color: #3670aa;
  font-size: 15px;
  padding-top: 20px;
  font-weight: 600;
}
.foot-btn:hover {
  color: #e6a23c;
  cursor: pointer;
}

.pwd-form {
  width: 400px;
  line-height: 50px;
}

.my-dialog {
  line-height: 50px;
  .input-block {
    width: 450px;
  }
  .el-dialog__footer {
    line-height: 50px;
  }
}
</style>
