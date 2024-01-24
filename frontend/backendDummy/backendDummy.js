import {createServer} from "http";
import {Server} from "socket.io";

/** @type {string} */
const logTag = "backendDummy:";

const io = new Server(createServer(), {
    cors: {
        origin: "http://localhost:8080",
    }
});

io.on('connection', (socket) => {
    console.log(logTag, 'Client connected');

    socket.on('disconnect', () => {
        console.log(logTag, 'Client disconnected');
    });

    socket.on("test.pass-through", () => {
        socket.emit("test.pass-through", JSON.stringify("received test event"));
    });
});

io.listen(8081);

console.log(logTag, 'WebSocket started on port 8081');