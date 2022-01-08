import Vue from "vue";
import Vuex from "vuex";
import api from "@/plugins/api";
import Socket from "./socket";
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
      sessionStorage.userInfo = JSON.stringify(userInfo);
      sessionStorage.token = userInfo.token;
    },
    logout(state) {
      state.token = null;
      state.currentUser = null;
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("userInfo");
    },
    SET_STATE(state, obj) {
      Object.keys(obj).forEach((k) => (state[k] = obj[k]));
    },
  },
  actions: {
    async getUserInfo({ commit }) {
      if (sessionStorage.currentUser) {
        const userInfo = await api.getUserInfo({
          user_id: sessionStorage.currentUser.user_id,
        });
        sessionStorage.userInfo = JSON.stringify(userInfo);
        commit("SET_STATE", { currentUser: userInfo });
      }
    },
  },
  modules: { Socket },
});
