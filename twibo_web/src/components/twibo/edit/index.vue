<template>
  <TwiboEditor ref="blogEditor"></TwiboEditor>
</template>
<script>
import TwiboEditor from "./editor.vue";
export default {
  name: "EditTwibo",
  components: { TwiboEditor },
  data() {
    return {
      saved: false,
      blogData: null,
    };
  },
  async beforeRouteLeave(to, from, next) {
    if (this.$refs.blogEditor.saved) {
      next();
    } else {
      const res = await this.$confirm("Are you sure to leave?", {
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        type: "warning",
      }).catch(() => {});
      if (res) {
        next();
      } else {
        return;
      }
    }
  },
};
</script>
