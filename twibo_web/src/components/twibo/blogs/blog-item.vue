<template>
  <div class="blog-item">
    <el-card>
      <div slot="header" class="blog-header">
        <div class="title">
          {{ blog.title }}
        </div>
        <div class="info">
          <el-avatar
            v-if="blog.author.avatar"
            :src="avatarSrc(blog.author.avatar)"
            :size="40"
            fit="contain"
          ></el-avatar>
          <el-avatar v-else :size="40">
            <span style="font-size: 30px"> <i class="el-icon-user"></i></span>
          </el-avatar>
          <div
            style="
              display: flex;
              flex-direction: column;
              align-items: flex-start;
              padding-left: 10px;
            "
          >
            <div style="font-weight: bolder; color: #2c3e50">
              {{ blog.author.name }}
            </div>
            <div style="color: #a6a6a8; font-size: 0.7rem">
              @{{ convertTime(blog.time) }}
            </div>
          </div>
        </div>
      </div>
      <div>
        {{ blog.abstract }}
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          icon="el-icon-view"
          @click="viewBlog"
          >View Detail</el-button
        >
      </div>
    </el-card>
  </div>
</template>
<script>
import { mapState } from "vuex";
import { avatarSrc, convertTime } from "@/utils/common";

export default {
  name: "BlogItem",
  props: ["blog"],
  data() {
    return {};
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendList: (state) => state.Friend.friendList,
    }),
  },
  methods: {
    convertTime,
    avatarSrc,
    viewBlog() {
      this.$router.push({
        name: "blogPage",
        params: { blog_id: this.blog.blog_id },
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.blog-item {
  padding: 20px;
}

.blog-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.title {
  font-weight: bolder;
  font-size: 1.5rem;
  color: #2c3e50;
}
.info {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 5px;
}
</style>
