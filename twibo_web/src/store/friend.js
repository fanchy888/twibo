import api from "@/plugins/api";
export default {
  state: {
    friendRequests: [],
    friendList: [],
  },
  mutations: {
    SET_STATE(state, obj) {
      Object.keys(obj).forEach((k) => (state[k] = obj[k]));
    },
  },
  actions: {
    async getFriendRequests({ rootState, commit }) {
      const { user_id } = rootState.currentUser;
      if (user_id) {
        const friendRequests = await api.getFriendRequests({ user_id });
        commit("SET_STATE", { friendRequests: friendRequests });
      }
    },
    async removeFriendRequest({ state, dispatch }, user_id) {
      state.friendRequests = state.friendRequests.filter(
        (f) => f.user_id !== user_id
      );
      dispatch("getFriends");
    },

    async getFriends({ rootState, commit }) {
      const user_id = rootState.currentUser.user_id;
      const friends = await api.getFriends({ user_id });
      commit("SET_STATE", { friendList: friends });
    },

    SOCKET_requestFriend({ state, rootState }, data) {
      const user = rootState.currentUser;
      if (user.user_id === data.receiver) {
        if (
          !state.friendRequests.filter((r) => r.user_id == data.sender.user_id)
            .length
        ) {
          state.friendRequests.push(data.sender);
        }
      }
    },
    SOCKET_clearRequest({ rootState, dispatch }, userList) {
      const user = rootState.currentUser;
      if (user.user_id === userList[0]) {
        let friend_id = userList[1];
        dispatch("removeFriendRequest", friend_id);
      } else if (user.user_id == userList[1]) {
        let friend_id = userList[0];
        dispatch("removeFriendRequest", friend_id);
      }
    },
  },
  getters: {},
};
