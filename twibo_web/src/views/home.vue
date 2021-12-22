<template>
  <div>home</div>
</template>
<script>
export default {
  name: "home",
  mounted() {
    this.$store.commit("logout");
  },
};
</script>
