import {createServer} from "http";
import {Server} from "socket.io";
import {EventError} from "../src/model/Error.js";

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

    socket.onAny((event, args) => {
        switch (event) {
            case "test-passthrough":
                socket.emit("test-passthrough", JSON.stringify("received test event"));
                break;
            default:
                socket.emit("error", JSON.stringify(new EventError(event, args)));
        }
    });
});

io.listen(8081);

console.log(logTag, 'WebSocket started on port 8081');