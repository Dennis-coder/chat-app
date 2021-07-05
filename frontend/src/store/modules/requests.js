export default {
	// namespaced: true,
	state: {
		requests: [],
		pendingRequests: []
	},
	mutations: {
		setRequests(state, requests) {
			state.requests = requests
		},
		setPendingRequests(state, requests) {
			state.pendingRequests = requests
		},
		addRequest(state, request) {
			state.requests.push(request)
		},
		addPendingRequest(state, request) {
			state.pendingRequests.push(request)
		},
		removeRequest(state, friendId) {
			let index = state.requests.findIndex(r => r.id === friendId)
			state.requests.splice(index, 1)
		},
		removePendingRequest(state, friendId) {
			let index = state.pendingRequests.findIndex(r => r.id === friendId)
			state.pendingRequests.splice(index, 1)
		},
	},
	actions: {
		setRequests({ commit }, requests) {
			commit('setRequests', requests)
		},
		setPendingRequests({ commit }, requests) {
			commit('setPendingRequests', requests)
		},
		addRequest({ commit }, request) {
			commit('addRequest', request)
		},
		addPendingRequest({ commit }, request) {
			commit('addPendingRequest', request)
		},
		removeRequest({ commit }, friendId) {
			commit('removeRequest', friendId)
		},
		removePendingRequest({ commit }, friendId) {
			commit('removePendingRequest', friendId)
		},
	},
	modules: {
	}
}