<template>
  <el-card shadow="always">
    <div>
      <el-avatar v-if="user.avatar" :size="100" :src="avatarUrl"></el-avatar>
      <div v-else style="font-size: 50px">
        <i class="el-icon-picture-outline"></i>
      </div>
      <div>
        <el-button round><i class="el-icon-camera"></i></el-button>
      </div>
    </div>
  </el-card>
</template>
<script>
import { currentUser } from "@/utils/user";

export default {
  name: "setting",
  computed: {
    user() {
      return currentUser();
    },
    avatarUrl() {
      return this.$staticUrl + this.user.avatar;
    },
  },
};
</script>
