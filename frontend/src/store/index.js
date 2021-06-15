import { io } from 'socket.io-client'
import { createStore } from 'vuex'
import jwt_decode from 'jwt-decode'
import axios from 'axios'

const token = localStorage.getItem('websnap.user')
const user = token ? jwt_decode(token) : null

axios.defaults.headers.common['Authorization'] = token ? "Bearer " + token : null

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
    tab: 0
  },
  mutations: {
    setUser(state, newUser) {
      state.user = newUser
    },
    setFriends(state, friends) {
      state.friends = friends
    },
    addFriend(state, friend) {
      state.friends.push(friend)
    },
    removeFriend(state, friendId) {
      let index = state.friends.findIndex(f => f.id = friendId)
      state.friends.splice(index, 1)
    },
    setGroups(state, groups) {
      state.groups = groups
    },
    addGroup(state, group) {
      state.groups.push(group)
    },
    removeGroup(state, groupId) {
      let index = state.groups.findIndex(g => g.id = groupId)
      state.groups.splice(index, 1)
    },
    setSocket(state, socket) {
      if (state.socket) {
        state.socket.disconnect()
      }
      state.socket = socket
    },
    setTab(state, tab) {
      state.tab = tab
    },
  },
  actions: {
    setUser({ commit }, userToken) {
      localStorage.setItem('websnap.user', userToken)
      axios.defaults.headers.common['Authorization'] = "Bearer " + userToken
      commit('setUser', jwt_decode(userToken))
      commit('setSocket', socketGen())
    },
    logout({ commit }) {
      localStorage.removeItem('websnap.user')
      axios.defaults.headers.common['Authorization'] = ""
      commit('setUser', null)
      commit('setSocket', null)
      commit('setFriends', [])
      commit('setGroups', [])
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
    addGroup({ commit }, group) {
      commit('addGroup', group)
    },
    removeGroup({ commit }, groupId) {
      commit('removeGroup', groupId)
    },
    setTab({ commit }, tab) {
      commit('setTab', tab)
    },
  },
  modules: {
  }
})
