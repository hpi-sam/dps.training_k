import {io} from "socket.io-client";

export const backendSocket = io("http://localhost:8081", {
    autoConnect: false,
});

backendSocket.on("connect", () => {
    console.log("Server connected");
});

backendSocket.on("disconnect", () => {
    console.log('Server disconnected');
});