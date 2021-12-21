import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
  },
  mutations: {
    login(state, token) {
      state.token = token;
      localStorage.token = token;
    },
    logout(state) {
      state.token = null;
      localStorage.removeItem("token");
    },
  },
  actions: {},
  modules: {},
});
