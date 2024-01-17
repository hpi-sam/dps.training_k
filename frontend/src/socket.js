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

socket.on("test.pass-through", (arg) => {
    /** @type {String} */
    const s = JSON.parse(arg);
    console.log(s);
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
 * @param {TrainerLogin} login
 */
export function trainerLogin(login) {
    socket.emit("trainer.login", JSON.stringify(login));
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
 * @param {PatientLogin} login
 */
export function patientLogin(login) {
    socket.emit("patient.login", JSON.stringify(login));
}

/**
 * @param {String} name
 */
export function addAction(name) {
    socket.emit("patient.action.add", JSON.stringify({exerciseCode: name}));
}