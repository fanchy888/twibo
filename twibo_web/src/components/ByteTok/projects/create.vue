<template>
  <div v-loading="loading">
    <el-form
      label-position="left"
      label-width="150px"
      :model="form"
      :rules="rules"
      ref="form"
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
        <el-button type="primary" @click="onSubmit('form')">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "createProject",

  data() {
    return {
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

  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
  },
  methods: {
    async onSubmit(formName) {
      this.$refs[formName].validate((valid) => valid);
      this.loading = true;
      try {
        await this.$api.createProject({
          $body: {
            name: this.form.name,
            theme: this.form.theme,
            owner: this.user.user_id,
          },
        });
        this.$emit("reloadProject");
      } finally {
        this.loading = false;
      }
      this.$emit("closeCreate");
    },
    onCancel() {
      this.form.name = "";
      this.form.theme = "";
      this.$emit("closeCreate");
    },
  },
};
</script>
<style lang="scss" scoped></style>
