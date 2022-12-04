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
        <div class="pop-info" v-loading="loading">
          <el-avatar
            shape="square"
            v-if="group.avatar"
            :src="avatarSrc(group.avatar)"
            :size="50"
            fit="contain"
          ></el-avatar>
          <el-avatar v-else :size="50" shape="square">
            <span style="font-size: 40px"><i class="el-icon-s-grid"></i></span>
          </el-avatar>
          <div style="padding-top: 10px; color: #a6a6a8; font-size: 10px">
            {{ group.description }}
          </div>
          <div class="line">
            <span>{{ group.name }}</span>
            <span class="line-icon" @click="groupVisible = true"
              ><i class="el-icon-setting"></i
            ></span>
          </div>

          <div style="padding-top: 40px">
            <el-button
              type="success"
              size="small"
              icon="el-icon-chat-dot-round"
              @click="jumpToChat()"
              >Chat</el-button
            >
            <el-button
              v-if="!editable"
              type="danger"
              size="small"
              icon="el-icon-delete"
              @click="leaveGroup()"
              >Leave</el-button
            >
            <el-button
              v-else
              type="danger"
              size="small"
              icon="el-icon-delete"
              @click="dismissGroup()"
              >Dismiss</el-button
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
    <el-dialog width="50%" :visible.sync="groupVisible" destroy-on-close>
      <div class="group-dialog" v-loading="editLoading">
        <el-upload
          action="a"
          :http-request="uploadGroupAvatar"
          :before-upload="beforeUpload"
          :show-file-list="false"
        >
          <div slot="trigger" class="upload">
            <el-tooltip effect="dark" :content="tooltipInfo" placement="top">
              <el-avatar
                v-if="group && group.avatar"
                :size="100"
                :src="avatarSrc(group.avatar)"
                fit="contain"
                class="ava-child"
              ></el-avatar>
              <el-avatar v-else :size="100" class="ava-child">
                <span style="font-size: 50px"
                  ><i class="el-icon-s-grid"></i
                ></span>
              </el-avatar>
            </el-tooltip>
          </div>
        </el-upload>

        <el-form v-model="groupForm" label-width="100px" label-position="right">
          <el-form-item label="Name:">
            <el-input
              :disabled="!editable"
              maxlength="20"
              v-model="groupForm.name"
              @blur="editGroup()"
            ></el-input>
          </el-form-item>
          <el-form-item label="Description:">
            <el-input
              :disabled="!editable"
              maxlength="50"
              type="textarea"
              v-model="groupForm.description"
              @blur="editGroup()"
            ></el-input>
          </el-form-item>
          <el-form-item label="Creator:">
            <el-tag type="info">{{ groupForm.owner }}</el-tag>
          </el-form-item>
        </el-form>
        <div class="members">
          <el-divider>Members</el-divider>
          <el-row :gutter="0" class="row">
            <el-col :span="3" v-for="(member, index) in members" :key="index">
              <el-tooltip
                effect="dark"
                :content="member.name"
                placement="top-start"
              >
                <el-avatar
                  v-if="member.avatar"
                  :src="avatarSrc(member.avatar)"
                  :size="50"
                  fit="contain"
                  shape="square"
                ></el-avatar>
                <el-avatar v-else :size="50" shape="square">
                  <span style="font-size: 30px"
                    ><i class="el-icon-user"></i
                  ></span>
                </el-avatar>
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :gutter="0">
            <el-col :span="3">
              <el-button icon="el-icon-plus" @click="clickAdd()"></el-button>
            </el-col>
            <el-col :span="3" v-if="editable">
              <el-button icon="el-icon-minus" @click="clickKick()"></el-button>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-dialog>
    <el-dialog
      width="40%"
      :visible.sync="memberVisible"
      @close="closeMemberDialog"
    >
      <div
        v-if="memberMode === 'add'"
        v-loading="editLoading"
        class="member-dialog"
      >
        Invite
        <div style="line-height: 50px; width: 400px">
          <el-input
            prefix-icon="el-icon-search"
            v-model="searchInfo"
            placeholder="search"
          ></el-input>
        </div>
        <el-checkbox-group v-model="checkedMembers" class="checkGroup">
          <el-checkbox
            v-for="(friend, index) in filterdFriends"
            :key="index"
            :label="friend.user_id"
            class="checkItem"
            :disabled="checked(friend.user_id)"
          >
            <div class="checkItem">
              <el-avatar
                v-if="friend.avatar"
                :src="avatarSrc(friend.avatar)"
                :size="30"
                fit="contain"
                shape="square"
              ></el-avatar>
              <el-avatar v-else :size="30" shape="square">
                <span style="font-size: 30px"
                  ><i class="el-icon-user"></i
                ></span>
              </el-avatar>
              <span style="font-size: 20px; padding-left: 5px">{{
                friend.nick_name || friend.name
              }}</span>
            </div>
          </el-checkbox>
        </el-checkbox-group>
        <div class="tag">
          <el-tag
            v-for="user_id in checkedMembers"
            :key="user_id"
            type="success"
            style="margin: 3px"
            closable
            @close="rmvTag(user_id)"
          >
            {{ findFriend(user_id).nick_name || findFriend(user_id).name }}
          </el-tag>
        </div>
        <div>
          <el-button @click="invite()" type="primary">Invite</el-button>
        </div>
      </div>
      <div v-else v-loading="editLoading" class="member-dialog">
        Kick Members
        <div style="line-height: 50px; width: 400px">
          <el-input
            prefix-icon="el-icon-search"
            v-model="searchInfo"
            placeholder="search"
          ></el-input>
        </div>
        <el-checkbox-group v-model="kickedMembers" class="checkGroup">
          <el-checkbox
            v-for="(member, index) in filterdMembers"
            :key="index"
            :label="member.user_id"
            class="checkItem"
          >
            <div class="checkItem">
              <el-avatar
                v-if="member.avatar"
                :src="avatarSrc(member.avatar)"
                :size="30"
                fit="contain"
                shape="square"
              ></el-avatar>
              <el-avatar v-else :size="30" shape="square">
                <span style="font-size: 30px"
                  ><i class="el-icon-user"></i
                ></span>
              </el-avatar>
              <span style="font-size: 20px; padding-left: 5px">{{
                member.name
              }}</span>
            </div>
          </el-checkbox>
        </el-checkbox-group>
        <div class="tag">
          <el-tag
            v-for="user_id in kickedMembers"
            :key="user_id"
            type="danger"
            style="margin: 3px"
            closable
            @close="rmvKickedTag(user_id)"
          >
            {{ findMember(user_id).name }}
          </el-tag>
        </div>
        <div>
          <el-button @click="kick()" type="danger">Kick</el-button>
        </div>
      </div>
    </el-dialog>
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
      loading: false,
      editLoading: false,
      groupVisible: false,
      memberVisible: false,
      memberMode: "add",
      checkedMembers: [],
      kickedMembers: [],
      searchInfo: "",
      groupForm: {
        name: this.group.name,
        description: this.group.description,
        owner: this.group.owner,
      },
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendList: (state) => state.Friend.friendList,
    }),
    tooltipInfo() {
      return this.group && this.group.avatar ? "点击修改头像" : "上传头像";
    },
    editable() {
      return this.user.user_id === this.group.creator;
    },

    filterdFriends() {
      return this.friendList.filter(
        (f) =>
          (f.nick_name && f.nick_name.includes(this.searchInfo)) ||
          f.name.includes(this.searchInfo)
      );
    },

    members() {
      return this.group.members.map((m) => {
        m.name = this.findFriend(m.user_id).nick_name || m.name;
        return m;
      });
    },

    filterdMembers() {
      return this.members.filter(
        (f) =>
          f.user_id !== this.group.creator &&
          ((f.nick_name && f.nick_name.includes(this.searchInfo)) ||
            f.name.includes(this.searchInfo))
      );
    },
  },

  methods: {
    avatarSrc: avatarSrc,
    beforeUpload(file) {
      const isValidType = ["image/jpeg", "image/png", "image/gif"].includes(
        file.type
      );

      if (!isValidType) {
        this.$message.error("请上传png/jpg/jpeg/gif格式的图片");
      }

      return isValidType;
    },
    async uploadGroupAvatar(param) {
      let data = new FormData();
      data.append("file", param.file);
      try {
        this.editLoading = true;
        const res = await this.$api.editGroupAvatar({
          $body: data,
          group_id: this.group.group_id,
        });
        if (res) {
          this.$message({
            type: "success",
            message: "上传成功",
            duration: 2000,
          });
          this.$store.dispatch("getOneGroup", this.group.group_id);
        }
      } finally {
        this.editLoading = false;
      }
    },
    async editGroup() {
      this.editLoading = true;
      try {
        const res = await this.$api.editGroup({
          group_id: this.group.group_id,
          $body: {
            name: this.groupForm.name,
            description: this.groupForm.description,
          },
        });
        if (res) {
          this.$store.dispatch("getOneGroup", this.group.group_id);
        }
      } finally {
        this.editLoading = false;
      }
    },
    rmvTag(user_id) {
      this.checkedMembers.splice(this.checkedMembers.indexOf(user_id), 1);
    },
    rmvKickedTag(user_id) {
      this.kickedMembers.splice(this.kickedMembers.indexOf(user_id), 1);
    },
    findFriend(user_id) {
      return this.friendList.find((f) => f.user_id === user_id) || {};
    },
    findMember(user_id) {
      return this.members.find((f) => f.user_id === user_id) || {};
    },
    clickAdd() {
      this.memberVisible = true;
      this.memberMode = "add";
    },
    clickKick() {
      this.memberVisible = true;
      this.memberMode = "kick";
    },
    checked(user_id) {
      return this.group.members.map((m) => m.user_id).includes(user_id);
    },
    closeMemberDialog() {
      this.checkedMembers = [];
      this.kickedMembers = [];
      this.searchInfo = "";
    },
    async invite() {
      this.editLoading = true;
      try {
        const res = await this.$api.addGroupMember({
          group_id: this.group.group_id,
          $body: this.checkedMembers,
        });
        if (res.success) {
          this.$store.dispatch("getOneGroup", this.group.group_id);
          this.$store.dispatch("getChatList");
          this.memberVisible = false;
        }
      } finally {
        this.editLoading = false;
      }
    },

    async kick() {
      this.editLoading = true;
      try {
        const res = await this.$api.kickGroupMember({
          group_id: this.group.group_id,
          $body: { user_ids: this.kickedMembers },
        });
        if (res.success) {
          this.$store.dispatch("getOneGroup", this.group.group_id);
          this.$store.dispatch("getChatList");
          this.memberVisible = false;
        }
      } finally {
        this.editLoading = false;
      }
    },

    async leaveGroup() {
      const yes = await this.$confirm("Are you fucking sure?", {
        confirmButtonText: "FUCK YOU ALL",
        cancelButtonText: "Just kidding",
        type: "warning",
      }).catch(() => {});
      if (!yes) {
        return;
      }
      this.loading = true;

      try {
        await this.$api.quitGroup({
          group_id: this.group.group_id,
          user_id: this.user.user_id,
        });
      } finally {
        this.loading = false;
      }
    },
    async dismissGroup() {
      const yes = await this.$confirm("Are you sure to dismiss this group?", {
        confirmButtonText: "They deserve it!",
        cancelButtonText: "Just kidding",
        type: "warning",
      }).catch(() => {});
      if (!yes) {
        return;
      }
      this.loading = true;
      try {
        await this.$api.deleteGroup({ group_id: this.group.group_id });
      } finally {
        this.loading = false;
      }
    },
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
.line {
  display: flex;
  align-items: center;
  font-size: 20px;
  .line-icon {
    padding-left: 10px;
  }
  .line-icon:hover {
    color: #409eff;
    cursor: pointer;
  }
}

.group-dialog {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.upload {
  height: 100px;
  & :hover {
    box-shadow: 0 0 10px #666;
  }
  .ava-child :hover {
    box-shadow: unset;
  }
}
.members {
  width: 60%;
  .row {
    line-height: 50px;
  }
}
.member-dialog {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.checkGroup {
  height: 300px;
  width: 400px;
  overflow-y: auto;
  border: solid 1px #eaecf1;
}
.checkItem {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 5px;
}
.tag {
  line-height: 50px;
  word-wrap: break-word;
  width: 400px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
</style>
