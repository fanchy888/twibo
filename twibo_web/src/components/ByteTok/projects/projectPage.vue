<template>
  <div>
    <el-page-header :content="project.name" @back="goBack"> </el-page-header>
    <el-divider><i class="el-icon-s-data"></i></el-divider>
    <div class="description">{{ project.theme }}</div>

    <taskItem
      v-for="(task, index) in tasks"
      :key="index"
      :task="task"
      @clickEdit="clickEdit"
    ></taskItem>

    <el-button
      style="margin-top: 20px"
      type="success"
      round
      @click="clickCreate"
      >Add Task</el-button
    >
    <el-dialog
      title="Create a Task"
      :visible.sync="taskVisible"
      destroy-on-close
      v-loading="loading"
      :show-close="false"
    >
      <el-form label-position="right" label-width="80px" :model="taskForm">
        <el-form-item label="name">
          <el-input v-model="taskForm.name" maxlength="500"></el-input>
        </el-form-item>
        <el-form-item label="detail">
          <el-input
            v-model="taskForm.content"
            type="textarea"
            :autosize="{ minRows: 3 }"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="taskVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitTask">Create</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import taskItem from "./task";
export default {
  name: "projectPage",
  components: { taskItem },
  data() {
    return {
      project_id: "",
      project: {},
      mode: "create",
      loading: false,
      tasks: [],
      taskForm: {
        name: "",
        content: "",
      },
      taskVisible: false,
    };
  },
  async mounted() {
    this.project_id = this.$route.params.project_id;
    this.project = await this.$api.getOneProject({
      project_id: this.project_id,
    });
    this.tasks = this.project.tasks;
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    clickCreate() {
      this.mode = "create";
      this.taskVisible = true;
    },
    clickEdit() {
      this.mode = "edit";
      this.taskVisible = true;
    },
    async submitTask(task_id) {
      this.loading = true;

      try {
        if (this.mode === "create") {
          await this.$api.createTask({
            project_id: this.project_id,
            $body: {
              title: this.taskForm.name,
              content: this.taskForm.content,
            },
          });
        } else {
          await this.$api.updateTask({
            project_id: this.project_id,
            task_id: task_id,
            $body: {
              title: this.taskForm.name,
              content: this.taskForm.content,
            },
          });
        }
        this.tasks = await this.$api.getTasks({ project_id: this.project_id });
      } finally {
        this.loading = false;
        this.taskVisible = false;
        this.taskForm.name = "";
        this.taskForm.content = "";
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.description {
  color: #999;
  font-size: 20px;
  padding: 20px;
}
</style>
