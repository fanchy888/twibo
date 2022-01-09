<template>
  <el-card shadow="always" class="card">
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
              :src="avatarUrl"
              class="ava-child"
            ></el-avatar>
            <el-avatar v-else :size="100" class="ava-child">
              <span style="font-size: 50px"><i class="el-icon-user"></i></span>
            </el-avatar>
          </el-tooltip>
        </div>
      </el-upload>
    </div>
    <div class="name">昵称：{{ user.name }}</div>
  </el-card>
</template>
<script>
import { mapActions, mapState } from "vuex";
export default {
  name: "setting",
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
    avatarUrl() {
      return this.user ? this.$staticUrl + this.user.avatar : "";
    },
    tooltipInfo() {
      return this.user && this.user.avatar ? "点击修改头像" : "上传头像";
    },
  },
  mounted() {
    if (!this.user) {
      this.getUserInfo();
    }
  },
  methods: {
    ...mapActions(["getUserInfo"]),
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
  },
};
</script>
<style lang="scss" scoped>
.card {
  font-family: "PingFang SC";
}
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
.name {
  padding: 10px;
  line-height: 20px;
}
</style>
