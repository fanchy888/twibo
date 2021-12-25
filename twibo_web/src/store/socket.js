export default {
  state: {
    usr: {},
    chatList: [],
    isConnect: false,
  },
  actions: {
    SOCKET_connect({ commit }) {
      commit("SOCKET_connect");
    },
  },
  mutations: {
    SOCKET_connect(state) {
      state.isConnect = true;
    },
  },
  getters: {},
};
