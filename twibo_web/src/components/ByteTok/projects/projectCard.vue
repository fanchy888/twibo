<template>
  <div class="card">
    <el-card>
      <div slot="header" class="header">
        <el-button type="text" @click="viewProject">
          <span class="title">{{ project.name }}</span></el-button
        >
        <el-button
          type="warning"
          circle
          plain
          @click="deleteProject"
          icon="el-icon-close"
          size="mini"
        ></el-button>
      </div>
      <div class="description">{{ project.theme }}</div>
      <el-divider><i class="el-icon-s-data"></i></el-divider>

      <div v-for="task in project.tasks" :key="task.task_id" class="task_item">
        <div class="taskTitle">
          {{ task.title }}
        </div>
        <el-progress
          :text-inside="true"
          :stroke-width="20"
          :percentage="task.progress"
          :color="customColorMethod"
          status="success"
          style="width: 60%"
        ></el-progress>
      </div>
    </el-card>
  </div>
</template>
<script>
export default {
  name: "projectCard",
  props: ["project"],
  data() {
    return {};
  },
  methods: {
    customColorMethod(percentage) {
      if (percentage < 50) {
        return "#e6a23c";
      } else {
        return "#67c23a";
      }
    },
    viewProject() {
      this.$router.push({
        name: "projectPage",
        params: { project_id: this.project.project_id },
      });
    },
    async deleteProject() {
      const res = await this.$confirm("Are you sure?", {
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        type: "warning",
      }).catch(() => {});
      if (res) {
        await this.$api.deleteProject({ project_id: this.project.project_id });
        this.$emit("reload");
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.card {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  font-size: 1.3rem;
}
.description {
  color: #999;
  font-size: 15px;
}
.task_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  .taskTitle {
    padding: 5px;
  }
}
</style>
