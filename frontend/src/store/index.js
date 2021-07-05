import { createStore } from 'vuex'
import axios from 'axios'
import jwt_decode from 'jwt-decode'
import { socketGen, setup } from '../sockets/index.js'
import groupsModule from './modules/groups.js'
import friendsModule from './modules/friends.js'
import requestsModule from './modules/requests.js'

export default createStore({
	state: {
		user: null,
		socket: null,
		tab: 0,
	},
	mutations: {
		setUser(state, newUser) {
			state.user = newUser
		},

		setSocket(state, socket) {
			if (state.socket) {
				state.socket.disconnect()
			}
			state.socket = socket
		},
		socketSetup(state) {
			setup(state.socket)
		},
		setTab(state, tab) {
			state.tab = tab
		},
	},
	actions: {
		login({ commit, dispatch }, userToken) {
			localStorage.setItem('websnap.user', userToken)
			axios.defaults.headers.common['Authorization'] = "Bearer " + userToken
			commit('setUser', jwt_decode(userToken))
			let socket = socketGen()
			commit('setSocket', socket)
			loadData(dispatch, socket)
			commit('socketSetup')
		},
		logout({ commit }) {
			localStorage.removeItem('websnap.user')
			axios.defaults.headers.common['Authorization'] = ""
			commit('setUser', null)
			commit('setSocket', null)
			commit('setFriends', [])
			commit('setGroups', [])
		},

		setTab({ commit }, tab) {
			commit('setTab', tab)
		},
	},
	modules: {
		groupsModule,
		friendsModule,
		requestsModule
	}
})

const loadData = async function (dispatch, socket) {
	let friends = (await axios.get("/api/v1/friends", { params: { includeMessages: true } })).data
	dispatch("setFriends", friends);

	let groups = (await axios.get("/api/v1/groups", { params: { includeMessages: true } })).data
	dispatch("setGroups", groups);

	groups.forEach((g) => {
		socket.emit('joinGroup', g.id)
	})

	let requests = (await axios.get("/api/v1/friend/requests")).data
	dispatch("setRequests", requests)
	
	let pendingRequests = (await axios.get("/api/v1/friend/requests/pending")).data
	dispatch("setPendingRequests", pendingRequests)
};