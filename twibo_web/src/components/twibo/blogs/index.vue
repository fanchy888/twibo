<template>
  <div>
    <div class="header">
      <el-button @click="edit" icon="el-icon-plus" round type="success"
        >Create</el-button
      >

      <el-input
        v-model="searchInfo"
        class="search"
        prefix-icon="el-icon-search"
        @change="searchBlogs"
      ></el-input>
    </div>
    <el-divider content-position="left">Twibo is not Weibo</el-divider>
    <ul
      v-infinite-scroll="loadBlogs"
      infinite-scroll-delay="1000"
      infinite-scroll-disabled="disabled"
      style="overflow: auto; height: 800px"
    >
      <BlogItem
        v-for="(blog, index) in blogList"
        :key="index"
        :blog="blog"
        class="infinite-list-item"
      >
      </BlogItem>
      <div v-loading="loading"></div>
    </ul>
  </div>
</template>
<script>
import { mapState } from "vuex";
import BlogItem from "./blog-item";
export default {
  name: "Blogs",
  components: { BlogItem },
  data() {
    return {
      blogList: [],
      page: 0,
      page_size: 10,
      loading: false,
      total: 0,
      searchInfo: "",
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendList: (state) => state.Friend.friendList,
    }),
    disabled() {
      return this.loading || this.blogList.length === this.total;
    },
  },
  async mounted() {
    const res = await this.$api.getBlogs({
      $query: { page_size: this.page_size, page: 0 },
    });
    this.blogList = res.blogs;
    this.total = res.total;
  },
  methods: {
    edit() {
      this.$router.push({ name: "edit" });
    },
    async searchBlogs() {
      this.page = 0;
      this.loading = true;
      try {
        const res = await this.$api.getBlogs({
          $query: {
            page_size: this.page_size,
            page: 0,
            keyword: this.searchInfo,
          },
        });
        this.blogList = res.blogs;
        this.total = res.total;
      } finally {
        this.loading = false;
      }
    },
    async loadBlogs() {
      if (this.blogList.length === this.total) {
        return;
      }
      this.loading = true;

      try {
        const newBlogs = await this.$api.getBlogs({
          $query: {
            page_size: this.page_size,
            page: this.page + 1,
            keyword: this.searchInfo,
          },
        });
        this.page++;
        this.total = newBlogs.total;
        this.blogList = this.blogList.concat(newBlogs.blogs);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.blog {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.search {
  width: 200px;
}

.header {
  display: flex;
  justify-content: space-between;
  padding-left: 20px;
  padding-right: 20px;
}
</style>
