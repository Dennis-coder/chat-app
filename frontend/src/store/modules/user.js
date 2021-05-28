import jwt_decode from 'jwt-decode'

let token = localStorage.getItem('websnap.user')

let user = token ? jwt_decode(token) : null

export default {
  state: {
    user: user
  },
  mutations: {
    setUser(state, newUser) {
      state.user = newUser
    }
  },
  actions: {
    setUser({ commit }, userToken) {
      localStorage.setItem('websnap.user', userToken)
      commit('setUser', jwt_decode(userToken))
    },
    removeUser({ commit }) {
      localStorage.removeItem('websnap.user')
      commit('setUser', null)
    }
  }
}
