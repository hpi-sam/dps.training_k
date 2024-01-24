import {io} from "socket.io-client";
import {logTag} from "./backendProxy.js";

export const backendSocket = io("http://localhost:8081", {
    autoConnect: false,
});

backendSocket.on("connect", () => {
    console.log(logTag, "Server connected");
});

backendSocket.on("disconnect", () => {
    console.log(logTag, 'Server disconnected');
});