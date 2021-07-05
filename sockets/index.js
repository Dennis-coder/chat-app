const jwt_decode = require('jwt-decode')
const io = require("socket.io")(3000, {
  cors: {
    origin: ["http://localhost:8080", "http://192.168.100.113:8080", "http://192.168.1.166:8080"]
  },
});

io.on('connection', (socket) => {
  console.log(`${socket.user.username} has connected and joined user-${socket.user.id}`);
  socket.join(`user-${socket.user.id}`)

  socket.on('disconnect', () => {
    console.log(`${socket.user.username} has disconnected`);
  });

  socket.on('chatMessage', (message) => {
    console.log(`message: ${message.text} to user-${message.recieverId}`);
    socket.to(`user-${message.recieverId}`).emit('newMessage', message);
  });

  socket.on('joinGroup', groupId => {
    group = `group-${groupId}`
    console.log(`${socket.user.username} joined ${group}`)
    socket.join(group)
  })

  socket.on('leaveGroup', groupId => {
    group = `group-${groupId}`
    console.log(`${socket.user.username} left ${group}`)
    socket.leave(group)
  })

  socket.on('groupMessage', (message) => {
    console.log(`group message: ${message.text}`);
    socket.to(`group-${message.groupId}`).emit('newGroupMessage', message);
  });

  socket.on('sentRequest', (recieverId) => {
    console.log(`${socket.user.username} sent a friend request to user-${recieverId}`)
    socket.to(`user-${recieverId}`).emit('newRequest', {id: socket.user.id, username: socket.user.username});
  })

  socket.on('acceptedRequest', (friendId) => {
    console.log(`${socket.user.username} accepted the friend request from user-${friendId}`)
    socket.to(`user-${friendId}`).emit('acceptedRequest', socket.user.id);
  })

  socket.on('deniedRequest', (friendId) => {
    console.log(`${socket.user.username} denied the friend request from user-${friendId}`)
    socket.to(`user-${friendId}`).emit('deniedRequest', socket.user.id);
  })

  socket.on('withdrewRequest', (friendId) => {
    console.log(`${socket.user.username} withdrew the friend request to user-${friendId}`)
    socket.to(`user-${friendId}`).emit('withdrewRequest', socket.user.id);
  })

  socket.on('removedFriend', (friendId) => {
    console.log(`${socket.user.username} removed user-${friendId} as a friend`)
    socket.to(`user-${friendId}`).emit('removedFriend', socket.user.id);
  })

  socket.on('newGroup', (group) => {
    console.log(`${socket.user.username} created a new group`)
    group.members.forEach((m) => {
      if (m.id != socket.user.id) {
        socket.to(`user-${m.id}`).emit('newGroup', group);
      }
    })
  })

  socket.on('removeGroup', (groupId) => {
    console.log(`${socket.user.username} removed group-${groupId}`)
    socket.to(`group-${groupId}`).emit('removeGroup', groupId);
  })

  socket.on('addUserToGroup', (group, user) => {
    console.log(`${socket.user.username} added user-${user.id} to group-${group.id}`)
    socket.to(`group-${group.id}`).emit('addUserToGroup', {groupId: group.id, user});
    socket.to(`user-${user.id}`).emit('newGroup', group);
  })

  socket.on('removeUserFromGroup', (groupId, userId) => {
    console.log(`${socket.user.username} removed user-${userId} from group-${groupId}`)
    socket.to(`group-${groupId}`).emit('removeUserFromGroup', groupId, userId);
    socket.to(`user-${userId}`).emit('removeGroup', groupId);
  })
});

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  const decoded = jwt_decode(token)
  socket.user = decoded;
  next();
});