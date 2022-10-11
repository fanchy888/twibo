import Vue from "vue";
import Vuex from "vuex";
import api from "@/plugins/api";
import Socket from "./socket";
import Friend from "./friend";
import Chat from "./chat";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
    currentUser: null,
  },
  mutations: {
    login(state, userInfo) {
      state.token = userInfo.token;
      state.currentUser = { ...userInfo };
      localStorage.setItem("token", userInfo.token);
    },
    logout(state) {
      state.token = null;
      state.currentUser = null;
      localStorage.removeItem("token");
      state.Friend.friendList = [];
      state.Friend.friendRequests = [];
      state.Chat.chatList = [];
      state.Chat.messages = {};
      state.Chat.currentChat = {};
    },
    SET_STATE(state, obj) {
      Object.keys(obj).forEach((k) => (state[k] = obj[k]));
    },
  },
  actions: {
    async getUserInfo({ commit }) {
      const user_id = localStorage.getItem("token");
      if (user_id) {
        const userInfo = await api.getUserInfo({
          $query: { user_id: user_id },
        });

        commit("SET_STATE", { currentUser: userInfo });
      }
    },
  },
  modules: { Socket, Friend, Chat },
});
