import {createServer} from "http";
import {Server} from "socket.io";

const io = new Server(createServer(), {
    cors: {
        origin: "http://localhost:8080",
    }
});

io.on('connection', (socket) => {
    console.log('Client connected');

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });

    socket.on("test.pass-through", () => {
        socket.emit("test.pass-through", JSON.stringify("received test event"));
    });
});

io.listen(8081);

console.log('WebSocket backendDummy started on port 8081');