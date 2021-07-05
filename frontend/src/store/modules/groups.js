export default {
	// namespaced: true,
	state: {
		groups: [],
	},
	mutations: {
		setGroups(state, groups) {
			state.groups = groups
		},
		addGroup(state, group) {
			state.groups.push(group)
		},
		removeGroup(state, groupId) {
			let index = state.groups.findIndex(g => g.id === groupId)
			state.groups.splice(index, 1)
		},

		addUserToGroup(state, {groupId, user}) {
			let index = state.groups.findIndex(g => g.id === groupId)
			state.groups[index].members.push(user)
		},
		removeUserFromGroup(state, groupId, userId) {
			let gIndex = state.groups.findIndex(g => g.id === groupId)
			let mIndex = state.groups[gIndex].members.findIndex(m => m.id === userId)
			state.groups[gIndex].members.splice(mIndex, 1)
		},

		addGroupMessage(state, message) {
			let index = state.groups.findIndex(g => g.id === message.groupId)
			state.groups[index].messages.push(message)
			state.groups[index].lastInteraction = message.timestamp
		},
	},
	actions: {
		setGroups({ commit }, groups) {
			commit('setGroups', groups)
		},
		addGroup({ commit }, group) {
			commit('addGroup', group)
		},
		removeGroup({ commit }, groupId) {
			commit('removeGroup', groupId)
		},

		addUserToGroup({ commit }, args) {
			commit('addUserToGroup', args)
		},
		removeUserFromGroup({ commit }, groupId, userId) {
			commit('removeUserFromGroup', groupId, userId)
		},

		addGroupMessage({ commit }, message) {
			commit('addGroupMessage', message)
		},
	},
	modules: {
	}
}