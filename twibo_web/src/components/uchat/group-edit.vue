<template>
  <div class="group" v-loading="loading">
    <div class="steps">
      <el-steps :active="step" finish-status="success" align-center>
        <el-step title="Basic"> </el-step>
        <el-step title="Members"> </el-step>
        <el-step title="Avatar"> </el-step>
      </el-steps>
    </div>
    <el-divider></el-divider>
    <div class="detail">
      <el-form
        ref="groupForm"
        :model="groupForm"
        label-width="100px"
        v-if="step === 0"
      >
        <el-form-item label="name">
          <el-input
            v-model="groupForm.name"
            maxlength="20"
            show-word-limit
            required
          ></el-input
        ></el-form-item>
        <el-form-item label="description">
          <el-input
            v-model="groupForm.description"
            type="textarea"
            maxlength="50"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <div v-else-if="step === 1" style="width: 400px">
        <div style="line-height: 50px">
          <el-input
            prefix-icon="el-icon-search"
            v-model="searchInfo"
            placeholder="search"
          ></el-input>
        </div>
        <el-checkbox-group v-model="checkedMembers" class="checkGroup">
          <el-checkbox
            :label="friend.user_id"
            v-for="(friend, index) in filterdFriends"
            :key="index"
            class="checkItem"
          >
            <div class="checkItem">
              <el-avatar :size="30" shape="square">
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
      </div>

      <el-upload
        action="a"
        :show-file-list="false"
        :auto-upload="false"
        :http-request="submit"
        :on-change="handleAvatarSuccess"
        :before-upload="beforeUpload"
        ref="uploadImg"
        v-else
        class="upload"
      >
        <div slot="trigger">
          <div class="img" v-if="imageUrl">
            <el-image
              :src="imageUrl"
              fit="cover"
              style="width: 200px; height: 200px"
            ></el-image>
          </div>
          <div class="img-default" v-else><i class="el-icon-camera"></i></div>
        </div>
      </el-upload>
    </div>
    <div class="foot">
      <el-button @click="last()" v-show="step > 0">
        <i class="el-icon-back"></i>
      </el-button>
      <el-button type="primary" @click="next()" v-show="step < 2">
        <i class="el-icon-right"></i>
      </el-button>
      <el-button type="primary" @click="submit()" v-show="step === 2"
        >Create</el-button
      >
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "groupEdit",
  data() {
    return {
      loading: false,
      step: 0,
      groupForm: { name: "", description: "" },
      title: "Create Group",
      checkedMembers: [],
      searchInfo: "",
      imageUrl: "",
      file: null,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.currentUser,
      friendRequests: (state) => state.Friend.friendRequests,
      friendList: (state) => state.Friend.friendList,
    }),
    filterdFriends() {
      return this.friendList.filter(
        (f) =>
          (f.nick_name && f.nick_name.includes(this.searchInfo)) ||
          f.name.includes(this.searchInfo)
      );
    },
  },
  methods: {
    ...mapActions(["getGroups", "getChatList"]),
    rmvTag(user_id) {
      this.checkedMembers.splice(this.checkedMembers.indexOf(user_id), 1);
    },
    findFriend(user_id) {
      return this.friendList.find((f) => f.user_id === user_id) || {};
    },
    next() {
      if (this.step === 2) {
        return;
      } else if (this.step === 0) {
        if (!this.groupForm.name) {
          this.$message.error("Name is required");
          return;
        }
      } else if (this.step === 1) {
        if (this.checkedMembers.length < 2) {
          this.$message.error("A group requires at least 2 other members");
          return;
        }
      }
      this.step += 1;
    },
    last() {
      if (this.step > 0) {
        this.step -= 1;
      }
    },

    async uploadImages() {
      let data = new FormData();
      this.fileList.forEach((file) => {
        data.append("file", file.raw);
      });

      try {
        this.loading = true;
        const res = await this.$api.uploadChatImg({
          $body: data,
          chat_id: this.chatInfo.chat_id,
        });

        res.forEach((msg) => {
          this.$socket.emit("chat", msg);
        });
      } finally {
        this.loading = false;
      }
    },
    beforeUpload(file) {
      const isValidType = ["image/jpeg", "image/png", "image/gif"].includes(
        file.raw.type
      );

      if (!isValidType) {
        this.$message.error("请上传png/jpg/jpeg/gif格式的图片");
      }

      return isValidType;
    },
    handleAvatarSuccess(file) {
      if (!this.beforeUpload(file)) {
        return false;
      }
      this.imageUrl = URL.createObjectURL(file.raw);
      this.file = file;
    },
    async submit() {
      this.loading = true;
      try {
        let data = new FormData();
        data.append("name", this.groupForm.name);
        data.append("description", this.groupForm.description);
        data.append("creator", this.user.user_id);
        this.checkedMembers.forEach((m) => data.append("members", m));

        if (this.file) {
          data.append("file", this.file.raw);
        }

        await this.$api.createGroup({ $body: data });
      } finally {
        this.loading = true;
      }
      this.$emit("closeDialog");
    },
  },
};
</script>
<style lang="scss" scoped>
.steps {
  line-height: 30px;
  padding-bottom: 20px;
}
.detail {
  padding-top: 20px;
  display: flex;
  justify-content: center;
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
}
.upload {
  height: 200px;
  width: 200px;
  line-height: 200px;

  .img {
    height: 200px;
    width: 200px;
    & :hover {
      box-shadow: 0 0 10px #666;
    }
  }
  .img-default {
    height: 200px;
    width: 200px;
    border: dashed 2px #eaecf1;
    border-radius: 6px;
    font-size: 30px;
  }
  .img-default:hover {
    border-color: #409eff;
  }
}

.foot {
  line-height: 20px;
  padding-top: 30px;
  text-align: end;
}
</style>
