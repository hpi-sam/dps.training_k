import {createServer} from "http";
import {Server} from "socket.io";

const mockBackend = new Server(createServer(), {
    cors: {
        origin: "http://localhost:5173",
    }
});

mockBackend.on('connection', (mockBackendSocket) => {
    console.log('Client connected');

    mockBackendSocket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

mockBackend.listen(8080);

console.log('Mock WebSocket backend started on port 8080');