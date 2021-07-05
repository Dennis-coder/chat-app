export default {
	// namespaced: true,
	state: {
		friends: [],
	},
	mutations: {
		setFriends(state, friends) {
			state.friends = friends
		},
		addFriend(state, friend) {
			state.friends.push(friend)
		},
		removeFriend(state, friendId) {
			let index = state.friends.findIndex(f => f.id === friendId)
			state.friends.splice(index, 1)
		},

		addMessage(state, message) {
			let index = state.friends.findIndex(f => f.id === message.senderId || f.id === message.recieverId)
			state.friends[index].messages.push(message)
			state.friends[index].lastInteraction = message.timestamp
		},
	},
	actions: {
		setFriends({ commit }, friends) {
			commit('setFriends', friends)
		},
		addFriend({ commit }, friend) {
			commit('addFriend', friend)
		},
		removeFriend({ commit }, friendId) {
			commit('removeFriend', friendId)
		},

		addMessage({ commit }, message) {
			commit('addMessage', message)
		},
	},
	modules: {
	}
}