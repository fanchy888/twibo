<template>
  <div v-if="project.name">
    <el-page-header :content="project.name" @back="goBack"> </el-page-header>
    <el-divider><i class="el-icon-s-data"></i></el-divider>

    <div class="description">
      {{ project.theme }}
    </div>
    <div class="switch">
      show archived
      <el-switch v-model="showArchived" active-color="#13ce66"> </el-switch>
    </div>
    <el-timeline>
      <el-timeline-item
        :timestamp="convertTime(task.create_date)"
        placement="top"
        v-for="(task, index) in filteredTasks"
        :key="task.name + index"
      >
        <taskItem
          :task="task"
          :project_id="project_id"
          @clickEdit="clickEdit(task)"
          @clickArchive="reloadTasks"
        ></taskItem>
      </el-timeline-item>
    </el-timeline>
    <el-button
      style="margin-top: 20px"
      type="success"
      round
      @click="clickCreate"
      >Add Task</el-button
    >
    <el-dialog
      :title="mode === 'create' ? 'Create' : 'Edit'"
      :visible.sync="taskVisible"
      destroy-on-close
      v-loading="loading"
      :show-close="false"
    >
      <el-form label-position="right" label-width="80px" :model="taskForm">
        <el-form-item label="title">
          <el-input v-model="taskForm.title" maxlength="500"></el-input>
        </el-form-item>
        <el-form-item label="content">
          <el-input
            v-model="taskForm.content"
            type="textarea"
            :autosize="{ minRows: 3 }"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="progress" v-if="selectedTask.task_id">
          <el-slider
            v-model="taskForm.progress"
            style="padding-left: 10px; width: 80%"
          ></el-slider>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="taskVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitTask()">Submit</el-button>
      </span>
    </el-dialog>
  </div>
  <el-empty v-else description="Byte will not dance"></el-empty>
</template>

<script>
import taskItem from "./task";
import { convertTime } from "@/utils/common";

export default {
  name: "projectPage",
  components: { taskItem },
  data() {
    return {
      project_id: "",
      project: {},
      mode: "create",
      loading: false,
      showArchived: false,
      tasks: [],
      selectedTask: {},
      taskForm: {
        title: "",
        content: "",
        progress: 0,
      },
      taskVisible: false,
    };
  },
  computed: {
    filteredTasks() {
      if (this.showArchived) {
        return this.tasks;
      } else {
        return this.tasks.filter((t) => !t.archived);
      }
    },
  },
  async mounted() {
    this.project_id = this.$route.params.project_id;
    this.project = await this.$api.getOneProject({
      project_id: this.project_id,
    });
    this.tasks = this.project.tasks;
  },
  methods: {
    convertTime,
    goBack() {
      this.$router.back();
    },
    clickCreate() {
      this.mode = "create";
      this.taskVisible = true;
      this.taskForm.title = "";
      this.taskForm.content = "";
      this.taskForm.progress = 0;
      this.selectedTask = {};
    },
    clickEdit(task) {
      this.mode = "edit";
      this.taskVisible = true;
      this.selectedTask = task;
      this.taskForm.title = task.title;
      this.taskForm.content = task.content;
      this.taskForm.progress = task.progress;
    },
    async submitTask() {
      this.loading = true;

      try {
        if (this.mode === "create") {
          await this.$api.createTask({
            project_id: this.project_id,
            $body: {
              title: this.taskForm.title,
              content: this.taskForm.content,
            },
          });
        } else {
          await this.$api.updateTask({
            project_id: this.project_id,
            task_id: this.selectedTask.task_id,
            $body: {
              title: this.taskForm.title,
              content: this.taskForm.content,
              progress: this.taskForm.progress,
            },
          });
        }
        await this.reloadTasks();
      } finally {
        this.loading = false;
        this.taskVisible = false;
        this.taskForm.name = "";
        this.taskForm.content = "";
        this.taskForm.progress = 0;
        this.selectedTask = {};
      }
    },

    async reloadTasks() {
      this.loading = true;
      try {
        this.tasks = await this.$api.getTasks({ project_id: this.project_id });
      } finally {
        this.loading = false;
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
.switch {
  color: #999;
  padding-bottom: 20px;
  text-align: right;
}
</style>
