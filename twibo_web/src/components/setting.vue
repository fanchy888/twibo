<template>
  <el-card shadow="always" style="height: 100%">
    <div class="avatar">
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
      <el-form-item label="昵称:">
        <el-input
          v-model="userForm.name"
          maxlength="20"
          show-word-limit
          @change="userForm.name = userForm.name.trim()"
        ></el-input>
      </el-form-item>
      <el-form-item label="签名:">
        <el-input
          v-model="userForm.description"
          maxlength="50"
          show-word-limit
          autosize
          @change="userForm.description = userForm.description.trim()"
          type="textarea"
        ></el-input>
      </el-form-item>
    </el-form>
    <el-button @click="updateInfo" type="primary" round plain class="btn"
      >Save</el-button
    >
  </el-card>
</template>
<script>
import { mapActions, mapState } from "vuex";
import { avatarSrc } from "@/utils/common";

export default {
  name: "setting",
  data() {
    return {
      loading: false,
      userForm: { name: "", description: "" },
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
  },
};
</script>
<style lang="scss" scoped>
.avatar {
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
  margin: auto;
  margin-top: 40px;
  margin-bottom: 10px;
}
</style>
