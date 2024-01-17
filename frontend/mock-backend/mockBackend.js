import {createServer} from "http";
import {Server} from "socket.io";
import {backendSocket} from "./backendSocket.js";
import {configureFrontendSocket} from "./frontendSocket.js";

const mockBackend = new Server(createServer(), {
    cors: {
        origin: "http://localhost:5173",
    }
});

mockBackend.on('connection', (s) => {
    console.log('Client connected');
    backendSocket.connect();

    s.on('disconnect', () => {
        console.log('Client disconnected');
        backendSocket.disconnect();
    });

    configureFrontendSocket(s);

    passThrough(s, backendSocket, "test");
});

mockBackend.listen(8080);

console.log('WebSocket mockBackend started on port 8080');


/**
 * Pass through events from frontend to backend and vice versa.
 * Should be used for every event that is already implemented in backend.
 * @param {Socket} frontendSocket
 * @param {Socket} backendSocket
 * @param {string} event
 */
function passThrough(frontendSocket, backendSocket, event) {
    frontendSocket.on(event, (args) => {
        backendSocket.emit(event, args);
    });
    backendSocket.on(event, (args) => {
        frontendSocket.emit(event, args);
    });
}