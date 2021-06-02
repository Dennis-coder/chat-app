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

  socket.on('chat message', (message) => {
    console.log(`message: ${message.text} to user-${message.recieverId}`);
    socket.to(`user-${message.recieverId}`).emit('incoming message', message);
  });

  socket.on('join-group', groupId => {
    group = `group-${groupId}`
    console.log(`joined ${group}`)
    socket.join(group)
  })

  socket.on('leave-group', groupId => {
    group = `group-${groupId}`
    console.log(`left ${group}`)
    socket.leave(group)
  })

  socket.on('group message', (message) => {
    console.log(`group message: message.text)`);
    socket.to(`group-${message.groupId}`).emit('group message', message);
  });
});

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  const decoded = jwt_decode(token)
  socket.user = decoded;
  next();
});