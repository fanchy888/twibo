<template>
  <div class="card" v-loading="loading">
    <el-card>
      <div slot="header" class="header">
        <el-button type="text" @click="viewProject">
          <span class="title">{{ project.name }}</span></el-button
        >
        <div>
          <el-button
            circle
            size="mini"
            plain
            icon="el-icon-edit"
            @click="clickEdit"
          ></el-button>
          <el-button
            type="warning"
            circle
            plain
            @click="deleteProject"
            icon="el-icon-close"
            size="mini"
          ></el-button>
        </div>
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
    <el-dialog
      title="Edit Project"
      :visible.sync="visible"
      center
      destroy-on-close
    >
      <el-form
        label-position="left"
        label-width="150px"
        :model="form"
        :rules="rules"
        ref="editForm"
      >
        <el-form-item label="Name" prop="name">
          <el-input
            v-model="form.name"
            clearable
            maxlength="100"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="Description" prop="theme">
          <el-input
            v-model="form.theme"
            type="textarea"
            :autosize="{ minRows: 3 }"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('editForm')"
            >Update</el-button
          >
          <el-button @click="visible = false">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "projectCard",
  props: ["project"],
  data() {
    return {
      name: "",
      description: "",
      visible: false,
      loading: false,
      form: { name: "", theme: "" },
      rules: {
        name: [
          { required: true, message: "Name is required", trigger: "blur" },
        ],
        theme: [
          {
            required: true,
            message: "Description is required",
            trigger: "blur",
          },
        ],
      },
    };
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
    clickEdit() {
      this.visible = true;
      this.form.name = this.project.name;
      this.form.theme = this.project.theme;
    },
    async onSubmit(formName) {
      this.$refs[formName].validate((valid) => valid);
      this.loading = true;
      try {
        await this.$api.updateProject({
          $body: {
            name: this.form.name,
            theme: this.form.theme,
          },
          project_id: this.project.project_id,
        });
        this.$emit("reload");
      } finally {
        this.loading = false;
        this.visible = false;
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
  word-break: break-all;
  word-wrap: break-word;
  white-space: pre-line;
}
.task_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  .taskTitle {
    padding: 5px;
    font-size: 13px;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    text-align: left;
  }
}
</style>
