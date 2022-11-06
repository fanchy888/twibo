import { timedelta } from "@/utils/common";
import api from "@/plugins/api";
import { showNotification } from "@/utils/notification";
import router from "@/router";
export default {
  state: {
    chatList: [],
    currentChat: {},
    messageList: {},
  },
  mutations: {
    SET_STATE(state, obj) {
      Object.keys(obj).forEach((k) => (state[k] = obj[k]));
    },
  },
  actions: {
    async getChatList({ rootState, commit }) {
      const param = { $query: { user_id: rootState.currentUser.user_id } };
      const chatList = await api.getChatList(param);
      commit("SET_STATE", { chatList: chatList });
      this._vm.$socket.emit("joinChat", rootState.currentUser.user_id);
    },

    addMessage({ rootState, state, commit }, msg) {
      const chatList = state.chatList;
      const chat_id = msg.chat_id;
      const chatRoom = chatList.find((c) => c.chat_id === chat_id) || {};
      const messages = chatRoom.messages || [];
      messages.push(msg);
      chatRoom.time = msg.time;
      if (
        chatRoom.members &&
        msg.sender !== rootState.currentUser.user_id &&
        router.app._route.name !== "uchat"
      ) {
        const sender = chatRoom.members.find((m) => m.user_id === msg.sender);
        const content = msg.type ? "You have a new message" : msg.content;
        showNotification(content, sender.name);
      }
      chatList.sort((a, b) => {
        return b["time"] - a["time"];
      });
      commit("SET_STATE", { chatList: chatList });
    },

    changeChatRoom({ commit }, chat) {
      chat.last_read = ((new Date().getTime() + timedelta) / 1000).toFixed();
      commit("SET_STATE", { currentChat: chat });
    },
    updateLastRead({ state, commit }) {
      const chat = state.currentChat;
      chat.last_read = ((new Date().getTime() + timedelta) / 1000).toFixed();
      commit("SET_STATE", { currentChat: chat });
    },
    SOCKET_chat({ dispatch }, receivedData) {
      dispatch("addMessage", receivedData);
    },

    SOCKET_createChat({ rootState, dispatch }, users) {
      if (users.find((x) => x === rootState.currentUser.user_id)) {
        dispatch("getChatList");
      }
    },
  },
  getters: {},
};
