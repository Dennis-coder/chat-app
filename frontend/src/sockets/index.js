import { io } from 'socket.io-client'
import store from '../store'
import axios from 'axios'

export function setup(socket) {
	socket.on(`newMessage`, (newMessage) => {
		store.dispatch('addMessage', newMessage)
	});
	socket.on(`newGroupMessage`, (newMessage) => {
		store.dispatch('addGroupMessage', newMessage)
	});
	socket.on('newRequest', (request) => {
		store.dispatch('addRequest', request)
	})
	socket.on('acceptedRequest', async (friendId) => {
		let friend = (await axios.get("/api/v1/friend", { params: { friend_id: friendId, includeMessages: true } })).data
		store.dispatch('addFriend', friend)
		store.dispatch('removePendingRequest', friend.id)
	})
	socket.on('deniedRequest', (friendId) => {
		store.dispatch('removePendingRequest', friendId)
	})
	socket.on('withdrewRequest', (friendId) => {
		store.dispatch('removeRequest', friendId)
	})
	socket.on('removedFriend', (friendId) => {
		store.dispatch('removeFriend', friendId)
	})
	socket.on('newGroup', (group) => {
		store.dispatch('addGroup', group)
		socket.emit('joinGroup', group.id)
	})
	socket.on('removeGroup', (groupId) => {
		store.dispatch('removeGroup', groupId)
		socket.emit('leaveGroup', groupId)
	})
	socket.on('addUserToGroup', (groupId, user) => {
		store.dispatch('addUserToGroup', groupId, user)
	})
	socket.on('removeUserFromGroup', (groupId, userId) => {
		store.dispatch('removeUserFromGroup', groupId, userId)
	})
}

export function socketGen() {
	const socketURL = window.location.host.slice(0, -5) + ':3000'
	return io(socketURL, { auth: { token: localStorage.getItem('websnap.user') } })
}