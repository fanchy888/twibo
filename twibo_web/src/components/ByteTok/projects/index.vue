<template>
  <div>
    <div class="header">
      <el-button
        type="primary"
        round
        icon="el-icon-document-add"
        @click="createVisible = true"
        >Create</el-button
      >
    </div>
    <el-divider content-position="right">Byte won't dance 💃</el-divider>

    <el-row v-for="(row, rowIndex) in projectRows" :key="rowIndex">
      <el-col :span="6" v-for="(project, index) in row" :key="index">
        <projectCard :project="project" @reload="getProjects"></projectCard>
      </el-col>
    </el-row>

    <el-dialog
      title="Create a new project"
      :visible.sync="createVisible"
      center
      destroy-on-close
    >
      <createProject
        @closeCreate="createVisible = false"
        @reloadProject="getProjects"
      ></createProject
    ></el-dialog>
  </div>
</template>
<script>
import createProject from "./create.vue";
import { mapState } from "vuex";
import ProjectCard from "./projectCard.vue";
export default {
  name: "Project",
  components: { createProject, ProjectCard },
  data() {
    return {
      projects: [],
      loading: false,
      createVisible: false,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
    projectRows() {
      const rows = [];
      this.projects.forEach((item, index) => {
        const row = Math.floor(index / 4);
        if (!rows[row]) {
          rows[row] = [];
        }
        rows[row].push(item);
      });
      return rows;
    },
  },
  async mounted() {
    this.projects = await this.$api.getProjects();
  },
  methods: {
    async getProjects() {
      this.projects = await this.$api.getProjects();
    },
  },
};
</script>
<style lang="scss" scoped>
.header {
  display: flex;
  justify-content: space-between;
  padding-left: 20px;
  padding-right: 20px;
}
</style>
