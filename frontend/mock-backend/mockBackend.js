import {createServer} from "http";
import {Server} from "socket.io";
import {backendSocket} from "./backendSocket.js";


const mockBackend = new Server(createServer(), {
    cors: {
        origin: "http://localhost:5173",
    }
});

mockBackend.on('connection', (frontendSocket) => {
    console.log('Client connected');

    backendSocket.connect();

    frontendSocket.on('disconnect', () => {
        console.log('Client disconnected');
        backendSocket.disconnect();
    });

    passThrough(frontendSocket, backendSocket, "test");

    frontendSocket.on("trainer.login", (args) => {
        const {username, password} = JSON.parse(args);
        const message = username === "test" && password === "test" ? "true" : "false";
        frontendSocket.emit("trainer.login.response", message);
    });

    frontendSocket.on("patient.login", (args) => {
        const {exerciseCode, patientCode} = JSON.parse(args);
        const message = exerciseCode === "123" && patientCode === "123" ? "true" : "false";
        frontendSocket.emit("patient.login.response", message);
    });
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