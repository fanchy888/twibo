<template>
  <div>
    <span class="btn" @click="dialogVisible = true">📷</span>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :v-loading="loading"
    >
      <el-upload
        action="a"
        :limit="9"
        :auto-upload="false"
        :on-exceed="handleExceed"
        :http-request="uploadImages"
        :on-change="beforeUpload"
        list-type="picture-card"
        ref="uploadImg"
      >
        <i class="el-icon-upload"></i>
      </el-upload>

      <span slot="footer" class="dialog-footer">
        <el-button @click="onCancel">Cancel</el-button>
        <el-button
          type="success"
          @click="onSend"
          :disabled="fileList.length == 0"
          >Send</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "uploadImg",
  props: ["chatInfo"],
  data() {
    return {
      dialogVisible: false,
      loading: false,
      fileList: [],
    };
  },
  computed: {
    title() {
      const l = this.fileList.length;
      return `Upload Images (${l}/9)`;
    },
  },
  methods: {
    handleExceed() {
      this.$message.warning("最多上传9张图片");
    },
    async uploadImages() {
      let data = new FormData();
      this.fileList.forEach((file) => {
        data.append("file", file.raw);
      });

      try {
        this.loading = true;
        const res = await this.$api.uploadChatImg({
          $body: data,
          chat_id: this.chatInfo.chat_id,
        });

        res.forEach((msg) => {
          this.$socket.emit("chat", msg);
        });
      } finally {
        this.loading = false;
      }
    },
    beforeUpload(file, fileList) {
      const isValidType = ["image/jpeg", "image/png", "image/gif"].includes(
        file.raw.type
      );

      if (!isValidType) {
        this.$message.error("请上传png/jpg/jpeg/gif格式的图片");
        fileList.pop();
      }
      this.fileList = fileList;
      return isValidType;
    },
    onCancel() {
      this.dialogVisible = false;
      this.$refs.uploadImg.clearFiles();
      this.fileList = [];
    },
    async onSend() {
      await this.uploadImages();
      this.fileList = [];
      this.dialogVisible = false;
      this.$refs.uploadImg.clearFiles();
      this.$emit("updateLastRead");
    },
  },
};
</script>
<style lang="scss" scoped>
.btn {
  padding-right: 2px;
}
.btn:hover {
  cursor: pointer;
}
</style>
