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

    SOCKET_requestFriend({ rootState }, data) {
      const user = rootState.currentUser;
      if (user.user_id === data.receiver) {
        rootState.friendRequests.push(data.sender);
      }
    },
  },
  mutations: {
    SOCKET_connect(state) {
      state.isConnect = true;
    },
    removeFriendRequest(state, user_id) {
      state.friendRequests = state.friendRequests.filter(
        (f) => f.user !== user_id
      );
    },
  },
  getters: {},
};
