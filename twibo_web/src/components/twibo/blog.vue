<template>
  <div>
    <div v-if="blog" v-loading="loading">
      <div class="back">
        <el-button
          type="warning"
          circle
          icon="el-icon-switch-button"
          plain
          @click="quit"
        ></el-button>
      </div>

      <div class="header">
        <el-avatar
          v-if="blog.author && blog.author.avatar"
          :src="avatarSrc(blog.author.avatar)"
          :size="40"
          fit="contain"
        ></el-avatar>
        <el-avatar v-else :size="40">
          <span style="font-size: 30px"> <i class="el-icon-user"></i></span>
        </el-avatar>
        <div class="info">{{ blog.author.name }}</div>

        <div class="title">{{ blog.title }}</div>
      </div>
      <el-divider></el-divider>
      <div class="content" v-html="blog.content"></div>
      <el-divider>
        <div style="color: #a6a6a8; font-size: 0.7rem">
          {{ convertTime(blog.time) }}
        </div></el-divider
      >
    </div>
    <el-empty description="Twibo is not Weibo" v-else></el-empty>
    <div v-if="isAuthor" class="footer">
      <el-button type="primary" icon="el-icon-edit" plain @click="editBlog"
        >Edit</el-button
      >
      <el-button type="danger" icon="el-icon-delete" plain @click="deleteBlog"
        >Delete</el-button
      >
    </div>
    <div v-else class="button">
      <el-button type="primary" circle icon="el-icon-thumb"></el-button>
      <el-button type="warning" circle icon="el-icon-cherry"></el-button>
      <el-button type="danger" circle icon="el-icon-chicken"></el-button>
    </div>
  </div>
</template>
<script>
import { avatarSrc, convertTime } from "@/utils/common";
import { mapState } from "vuex";

export default {
  name: "BlogPage",

  data() {
    return {
      blog: null,
      loading: false,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendList: (state) => state.Friend.friendList,
    }),
    isAuthor() {
      return (
        this.blog && this.user && this.user.user_id === this.blog.author.user_id
      );
    },
  },
  async mounted() {
    this.blog = await this.$api.getOneBlog({
      blog_id: this.$route.params.blog_id,
    });
  },
  methods: {
    avatarSrc,
    convertTime,
    async deleteBlog() {
      const yes = await this.$confirm("Are you sure to delete?", {
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        type: "warning",
      }).catch(() => {});

      if (yes) {
        this.loading = true;
        try {
          const res = await this.$api.deleteBlog({
            blog_id: this.blog.blog_id,
          });
          if (res) {
            this.$router.replace("/twibo");
          }
        } finally {
          this.loading = false;
        }
      }
    },
    editBlog() {
      this.$router.push({
        name: "editBlog",
        params: { blog_id: this.blog.blog_id },
      });
    },
    quit() {
      this.$router.push({ name: "twibo" });
    },
  },
};
</script>
<style lang="scss" scoped>
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.back {
  text-align: right;
}
.title {
  font-weight: bolder;
  font-size: 2rem;
  color: #2c3e50;
}
.content {
  padding-bottom: 20px;
}
.footer {
  text-align: right;
}
.button {
  display: flex;
}
</style>
