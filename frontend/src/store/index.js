import { io } from 'socket.io-client'
import { createStore } from 'vuex'
import userModule from './modules/user.js'

export default createStore({
  state: {
    friends: [],
    groups: [],
    socket: io(window.location.host.slice(0, -5) + ':3000')
  },
  mutations: {
    setFriends(state, friends){
      state.friends = friends
    },
    setGroups(state, groups){
      state.groups = groups
    },
    emitSocketEvent(state, args) {
      state.socket.emit(args.event, args.args);
    }
  },
  actions: {
    setFriends({ commit }, friends) {
      commit('setFriends', friends)
    },
    setGroups({ commit }, groups) {
      commit('setGroups', groups)
    },
    emitSocketEvent({ commit }, args) {
      commit('emitSocketEvent', args)
    }
  },
  modules: {
    userModule
  }
})
