<template>
  <div class="editor" v-loading="loading">
    <el-tag type="info" effect="light"> Title: </el-tag>
    <el-input
      v-model="title"
      maxlength="50"
      show-word-limit
      class="title"
    ></el-input>

    <el-tag type="info" effect="light"> Abstract: </el-tag>
    <el-input
      v-model="abstract"
      type="textarea"
      :rows="2"
      maxlength="200"
      show-word-limit
      class="title"
    ></el-input>

    <el-tag type="info" effect="light"> Content: </el-tag>
    <ckeditor
      :editor="editor"
      v-model="editorData"
      :config="editorConfig"
    ></ckeditor>
    <div class="btn">
      <el-button type="" plain @click="cancel">Cancel</el-button>

      <el-button type="primary" @click="save">Save</el-button>
    </div>
  </div>
</template>
<script>
import Editor from "ckeditor5-custom-build/build/ckeditor";
import { MyCustomUploadAdapterPlugin } from "./image-uploader";
import { mapState } from "vuex";

export default {
  name: "TwiboEditor",
  components: {},

  data() {
    return {
      loading: false,
      editMode: false,
      blog_id: null,
      title: "",
      abstract: "",
      saved: false,
      editor: Editor,
      editorData: "",
      editorConfig: {
        extraPlugins: [MyCustomUploadAdapterPlugin],
        // The configuration of the editor.
      },
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
  },
  async mounted() {
    this.blog_id = this.$route.params.blog_id;
    if (this.blog_id) {
      this.editMode = true;
      this.loading = true;
      try {
        const blog = await this.$api.getOneBlog({ blog_id: this.blog_id });
        if (blog) {
          this.title = blog.title;
          this.abstract = blog.abstract;
          this.editorData = blog.content;
        }
      } finally {
        this.loading = false;
      }
    }
  },
  methods: {
    async save() {
      this.loading = true;
      try {
        if (!this.title) {
          this.$message.error("A Title is required");
          return;
        }
        if (!this.editorData) {
          this.$message.error("Content is required");
          return;
        }
        const body = {
          title: this.title,
          abstract: this.abstract,
          content: this.editorData,
          author: this.user.user_id,
        };
        if (this.editMode) {
          await this.$api.updateBlog({ $body: body, blog_id: this.blog_id });
        } else {
          await this.$api.createBlog({ $body: body });
        }
        this.saved = true;
        this.$router.replace("/twibo");
      } finally {
        this.loading = false;
        this.saved = false;
      }
    },
    async cancel() {
      const res = await this.$confirm("Are you sure to leave?", {
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        type: "warning",
      }).catch(() => {});
      if (res) {
        this.saved = true;

        this.$router.replace("/twibo");
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.btn {
  text-align: right;
  padding-top: 20px;
}

.title {
  padding-bottom: 20px;
}
</style>
