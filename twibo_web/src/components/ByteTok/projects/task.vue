<template>
  <div class="card" v-loading="loading">
    <el-card v-if="!task.archived">
      <div class="header">
        <div class="title">{{ task.title }}</div>
        <el-tooltip effect="dark" content="Archive" placement="top">
          <el-button
            type="success"
            circle
            @click="archiveTask"
            icon="el-icon-check"
            size="mini"
          ></el-button>
        </el-tooltip>
      </div>
      <el-divider content-position="left"></el-divider>
      <div class="content">
        {{ task.content }}
      </div>
      <div class="footer">
        <el-progress
          :text-inside="true"
          :stroke-width="20"
          :percentage="task.progress"
          :color="customColorMethod"
          status="success"
          style="width: 60%"
        ></el-progress>
        <el-button
          @click="clickEdit"
          size="mini"
          icon="el-icon-edit"
          type="primary"
          >Edit</el-button
        >
      </div>
    </el-card>
    <el-card v-else>
      <div class="header">
        <div class="title-archive">{{ task.title }} (Archived)</div>
        <el-button
          type="success"
          circle
          icon="el-icon-check"
          size="mini"
          disabled
        ></el-button>
      </div>
      <el-divider content-position="left"></el-divider>
      <div class="content-archive">{{ task.content }}</div>
      <div class="footer">
        <el-progress
          :text-inside="true"
          :stroke-width="20"
          :percentage="task.progress"
          color="#909399"
          status="success"
          style="width: 60%"
        ></el-progress>
        <el-button @click="clickEdit" disabled size="mini" icon="el-icon-edit"
          >Edit</el-button
        >
      </div>
    </el-card>
  </div>
</template>
<script>
export default {
  name: "taskItem",
  props: ["task", "project_id"],
  data() {
    return {
      loading: false,
      progress: 0,
    };
  },

  methods: {
    customColorMethod(percentage) {
      if (percentage <= 50) {
        return "#e6a23c";
      } else {
        return "#67c23a";
      }
    },
    async archiveTask() {
      const res = await this.$confirm("Are you sure to archive this task?", {
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        type: "warning",
      }).catch(() => {});

      if (!res) {
        return;
      }
      this.loading = true;

      try {
        await this.$api.deleteTask({
          task_id: this.task.task_id,
          project_id: this.project_id,
        });
        this.$emit("clickArchive");
      } finally {
        this.loading = false;
      }
    },
    clickEdit() {
      this.$emit("clickEdit");
    },
  },
};
</script>
<style lang="scss" scoped>
.card {
  padding: 5px;
}
.header {
  display: flex;
  justify-content: space-between;
  .title {
    color: rgb(84, 92, 100);
    font-weight: 600;
  }
  .title-archive {
    font-weight: 600;
    color: #a6a6a8;
  }
}
.content {
  padding-bottom: 20px;
  color: rgb(84, 92, 100);
}
.content-archive {
  padding-bottom: 20px;

  color: #a6a6a8;
}
.footer {
  display: flex;
  justify-content: space-between;
}
</style>
