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
});

io.listen(8081);

console.log('WebSocket dummyBackend started on port 8081');