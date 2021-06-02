import { io } from 'socket.io-client'
import { createStore } from 'vuex'
import jwt_decode from 'jwt-decode'

const token = localStorage.getItem('websnap.user')
const user = token ? jwt_decode(token) : null

const socketGen = function () {
  const socketURL = window.location.host.slice(0, -5) + ':3000'
  return io(socketURL, { auth: { token: localStorage.getItem('websnap.user') } })
}

const socket = user ? socketGen() : null

export default createStore({
  state: {
    user,
    friends: [],
    groups: [],
    socket,
  },
  mutations: {
    setUser(state, newUser) {
      state.user = newUser
    },
    setFriends(state, friends) {
      state.friends = friends
    },
    addFriend(state, friend) {
      state.friends.unshift(friend)
    },
    removeFriend(state, friendId) {
      let index = state.friends.findIndex(f => f.id = friendId)
      state.friends.splice(index, 1)
    },
    setGroups(state, groups) {
      state.groups = groups
    },
    setSocket(state, socket) {
      if (state.socket) {
        state.socket.disconnect()
      }
      state.socket = socket
    }
  },
  actions: {
    setUser({ commit }, userToken) {
      localStorage.setItem('websnap.user', userToken)
      commit('setUser', jwt_decode(userToken))
      commit('setSocket', socketGen())
    },
    removeUser({ commit }) {
      localStorage.removeItem('websnap.user')
      commit('setUser', null)
      commit('setSocket', null)
    },
    setFriends({ commit }, friends) {
      commit('setFriends', friends)
    },
    addFriend({ commit }, friend) {
      commit('addFriend', friend)
    },
    removeFriend({ commit }, friendId) {
      commit('removeFriend', friendId)
    },
    setGroups({ commit }, groups) {
      commit('setGroups', groups)
    },
  },
  modules: {
  }
})
