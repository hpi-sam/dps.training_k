import {createServer} from "http";
import {Server} from "socket.io";
import {backendSocket} from "./backendSocket.js";


const mockBackend = new Server(createServer(), {
    cors: {
        origin: "http://localhost:5173",
    }
});

mockBackend.on('connection', (mockBackendSocket) => {
    console.log('Client connected');

    backendSocket.connect();

    mockBackendSocket.on('disconnect', () => {
        console.log('Client disconnected');
        backendSocket.disconnect();
    });
});

mockBackend.listen(8080);

console.log('WebSocket mockBackend started on port 8080');