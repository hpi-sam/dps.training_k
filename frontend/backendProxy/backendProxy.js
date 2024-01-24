import {createServer} from "http";
import {Server} from "socket.io";
import {backendSocket} from "./backendSocket.js";
import {configureTestEventListener, mockResponse} from "./frontendSocket.js";

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

    configureTestEventListener(frontendSocket);

    frontendSocket.onAny((event, args) => {
        if (event === "test-event") return; // ignore requested test events
        backendSocket.emit(event, args);
    });
    backendSocket.onAny((event, args) => {
        if (event === "error") {
            /** @type {EventError} */
            const error = JSON.parse(args);
            mockResponse(frontendSocket, error.event, error.args);
        } else {
            frontendSocket.emit(event, args);
        }
    });

});

backendProxy.listen(8080);

console.log(logTag, 'WebSockets started on port 8080');