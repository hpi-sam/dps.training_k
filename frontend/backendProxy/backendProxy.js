import {createServer} from "http";
import {Server} from "socket.io";
import {backendSocket} from "./backendSocket.js";
import {configureFrontendSocket} from "./frontendSocket.js";

/** @type {string} */
export const logTag = "backendProxy:";

const backendProxy = new Server(createServer(), {
    cors: {
        origin: "http://localhost:5173",
    }
});

backendProxy.on('connection', (frontendSocket) => {
    console.log(logTag, 'Client connected');
    backendSocket.connect();

    frontendSocket.on('disconnect', () => {
        console.log(logTag, 'Client disconnected');
        backendSocket.disconnect();
    });

    configureFrontendSocket(frontendSocket);

    passThrough(frontendSocket, backendSocket, "test-passthrough");
});

backendProxy.listen(8080);

console.log(logTag, 'WebSockets started on port 8080');


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