import {reactive} from "vue";
import {io} from "socket.io-client";

export const state = reactive({
    connected: false,
    fooEvents: [],
    barEvents: []
});

export const socket = io("http://localhost:8080", {
    autoConnect: false,
});

socket.on("connect", () => {
    state.connected = true;
    console.log("Server connected");
});

socket.on("disconnect", () => {
    state.connected = false;
    console.log("Server disconnected");
});
