import {reactive} from "vue";
import {io} from "socket.io-client";

/** @type {String} */
const logTag = "frontendSocket:";

export const state = reactive({
    connected: false,
});

export const socket = io("http://localhost:8080");

socket.on("connect", () => {
    state.connected = true;
    console.log(logTag, "Server connected");
});

socket.on("disconnect", () => {
    state.connected = false;
    console.log(logTag, "Server disconnected");
});

socket.on("test.pass-through", (arg) => {
    /** @type {String} */
    const s = JSON.parse(arg);
    console.log(logTag, "test.pass-through", s);
});

socket.on("trainer.login.response", (arg) => {
    /** @type {boolean} */
    const bool = JSON.parse(arg);
    console.log(logTag, "trainer.login.response", bool);
});

socket.on("patient.login.response", (arg) => {
    /** @type {boolean} */
    const bool = JSON.parse(arg);
    console.log(logTag, "patient.login.response", bool);
});

socket.on("trainer.exercise.create", (arg) => {
    /** @type {Exercise} */
    const exercise = JSON.parse(arg);
    console.log(logTag, "trainer.exercise.create", exercise);
});

socket.on("trainer.exercise.start", () => {
    console.log(logTag, "trainer.exercise.start");
});

socket.on("trainer.exercise.stop", () => {
    console.log(logTag, "trainer.exercise.stop");
});

socket.on("patient.load.notRunning", (arg) => {
    /** @type {PatientLoadNotRunning} */
    const patientLoad = JSON.parse(arg);
    console.log(logTag, "patient.load.notRunning", patientLoad);
});

socket.on("patient.load.running", (arg) => {
    /** @type {PatientLoadRunning} */
    const patientLoad = JSON.parse(arg);
    console.log(logTag, "patient.load.running", patientLoad);
});

socket.on("patient.phaseChange", (arg) => {
    /** @type {PatientPhaseChange} */
    const patientUpdate = JSON.parse(arg);
    console.log(logTag, "patient.phaseChange", patientUpdate);
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

export const serverEvents = {
    trainerExerciseCreate: "trainer.exercise.create",
    trainerExerciseStart: "trainer.exercise.start",
    trainerExerciseStop: "trainer.exercise.stop",
    patientLoadNotRunning: "patient.load.notRunning",
    patientLoadRunning: "patient.load.running",
    patientPhaseChange: "patient.phaseChange",
}