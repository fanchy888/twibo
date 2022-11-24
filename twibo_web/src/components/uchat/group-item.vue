<template>
  <div class="group-item">
    <el-avatar
      v-if="group.avatar"
      :src="avatarSrc(group.avatar)"
      :size="40"
      fit="contain"
      shape="square"
    ></el-avatar>
    <el-avatar v-else :size="40" shape="square">
      <span style="font-size: 30px"><i class="el-icon-s-grid"></i></span>
    </el-avatar>
    <div class="info">
      <span style="text-overflow: ellipsis; overflow: hidden">{{
        group.name
      }}</span>
      <el-popover placement="right" width="350" ref="popRef">
        <div class="pop-info" v-loading="editLoading">
          <el-avatar
            shape="square"
            v-if="group.avatar"
            :src="avatarSrc(group.avatar)"
            :size="50"
            fit="contain"
          ></el-avatar>
          <el-avatar v-else :size="50" shape="square">
            <span style="font-size: 40px"><i class="el-icon-user"></i></span>
          </el-avatar>
          <div style="padding-top: 10px; color: #a6a6a8; font-size: 10px">
            {{ group.description }}
          </div>
          <div style="padding-top: 10px">
            {{ group.name }}
          </div>
          <div style="padding-top: 10px">
            alias:
            <el-button
              type=""
              icon="el-icon-edit"
              circle
              size="mini"
              @click="editName = true"
              style="margin-left: 5px"
            ></el-button>
          </div>
          <div style="padding-top: 50px">
            <el-button
              type="success"
              size="small"
              icon="el-icon-chat-dot-round"
              @click="jumpToChat(group, index)"
              >Chat</el-button
            >
            <el-button
              type="danger"
              size="small"
              icon="el-icon-delete"
              @click="clickDelete(group)"
              >Leave</el-button
            >
            <el-button
              type="warning"
              size="small"
              icon="el-icon-delete-solid"
              v-if="user.user_id !== group.creator"
              @click="clickDissmiss(group)"
              >Dissmiss</el-button
            >
          </div>
        </div>

        <el-button
          slot="reference"
          icon="el-icon-more"
          circle
          size="mini"
        ></el-button>
      </el-popover>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { avatarSrc } from "@/utils/common";
export default {
  name: "groupChat",
  props: ["group", "index"],
  data() {
    return {
      editLoading: false,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
    }),
  },
  methods: {
    avatarSrc: avatarSrc,
    jumpToChat() {
      this.$refs.popRef.doClose();
      this.$emit("jumpToChat", this.group);
    },
  },
};
</script>
<style lang="scss" scoped>
.group-item {
  width: auto;
  height: 50px;
  line-height: 50px;
  display: flex;
  align-items: center;
  border-bottom: solid 1px #eaecf1;
}
.group-item:hover {
  background: #ececea;
}
.info {
  padding-left: 15px;
  font-size: 18px;
  color: rgb(84, 92, 100);
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  width: 200px;
}
.pop-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: auto;
}
</style>
