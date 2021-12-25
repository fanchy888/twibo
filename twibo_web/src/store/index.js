import Vue from "vue";
import Vuex from "vuex";
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
      sessionStorage.currentUser = userInfo;
      sessionStorage.token = userInfo.token;
    },
    logout(state) {
      state.token = null;
      state.currentUser = null;
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("currentUser");
    },
  },
  actions: {},
  modules: { Socket },
});
