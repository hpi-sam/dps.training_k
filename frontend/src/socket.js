import {reactive} from "vue";
import {io} from "socket.io-client";

export const state = reactive({
    connected: false,
});

export const socket = io("http://localhost:8080");

socket.on("connect", () => {
    state.connected = true;
    console.log("Server connected");
});

socket.on("disconnect", () => {
    state.connected = false;
    console.log("Server disconnected");
});

socket.on("test", (arg) => {
    console.log(arg);
});

socket.on("trainer.login.response", (arg) => {
    /** @type {boolean} */
    const bool = JSON.parse(arg);
    console.log(bool);
});

socket.on("patient.login.response", (arg) => {
    /** @type {boolean} */
    const bool = JSON.parse(arg);
    console.log(bool);
});

/**
 * @param {String} username
 * @param {String} password
 */
export function trainerLogin(username, password) {
    socket.emit("trainer.login", JSON.stringify({username: username, password: password}));
}

export function trainerCreateExercise() {
    socket.emit("trainer.exercise.create");
}

export function trainerStartExercise() {
    socket.emit("trainer.exercise.start");
}

export function trainerExerciseStop() {
    socket.emit("trainer.exercise.stop");
}

/**
 * @param {String} exerciseCode
 * @param {String} patientCode
 */
export function patientLogin(exerciseCode, patientCode) {
    socket.emit("patient.login", JSON.stringify({exerciseCode: exerciseCode, patientCode: patientCode}));
}

/**
 * @param {String} name
 */
export function addAction(name) {
    socket.emit("patient.action.add", JSON.stringify({exerciseCode: name}));
}