const httpServer = require("http").createServer();
const io = require("socket.io")(httpServer, {
  cors: {
    origin: ["http://localhost:8080", "http://192.168.100.113:8080"]
  },
});

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });

  socket.on('chat message', (args) => {
    console.log('message: ' + args.data.text);
    socket.broadcast.emit(args.event, args.data);
  });
});

// io.use((socket, next) => {
//   const username = socket.handshake.auth.username;
//   if (!username) {
//     return next(new Error("invalid username"));
//   }
//   socket.username = username;
//   next();
// });

// io.on("connection", (socket) => {
//   // fetch existing users
//   const users = [];
//   for (let [id, socket] of io.of("/").sockets) {
//     users.push({
//       userID: id,
//       username: socket.username,
//     });
//   }
//   socket.emit("users", users);

//   // notify existing users
//   socket.broadcast.emit("user connected", {
//     userID: socket.id,
//     username: socket.username,
//   });

//   // forward the private message to the right recipient
//   socket.on("private message", ({ content, to }) => {
//     socket.to(to).emit("private message", {
//       content,
//       from: socket.id,
//     });
//   });

//   // notify users upon disconnection
//   socket.on("disconnect", () => {
//     socket.broadcast.emit("user disconnected", socket.id);
//   });
// });

const PORT = process.env.PORT || 3000;

httpServer.listen(PORT, () =>
  console.log(`server listening at http://localhost:${PORT}`)
);