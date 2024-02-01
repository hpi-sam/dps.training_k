import {reactive} from "vue";
import {io} from "socket.io-client";
import { useExerciseStore } from "./stores/Exercise.js";
import {showErrorToast, showWarningToast} from "@/App.vue";

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

export function configureSocket() {
    const exerciseStore = useExerciseStore()
    
    socket.on("test-passthrough", (arg) => {
		/** @type {String} */
		const s = JSON.parse(arg);
		console.log(logTag, "test-passthrough", s);
	});

	socket.on("mock", (arg) => {
		/** @type {String} */
		const event = JSON.parse(arg);
		showWarningToast("Mocked event: " + event);
	});

	socket.on("error", (arg) => {
		/** @type {EventError} */
		const error = JSON.parse(arg);
		showErrorToast("Error on event: " + error.event);
	});

	socket.on("trainer-login", (arg) => {
		/** @type {boolean} */
		const bool = JSON.parse(arg);
		console.log(logTag, "trainer-login", bool);
	});

	socket.on("patient-login", (arg) => {
		/** @type {boolean} */
		const bool = JSON.parse(arg);
		console.log(logTag, "patient-login", bool);
	});

	socket.on("trainer.exercise.create", (arg) => {
		const json = JSON.parse(arg)
		exerciseStore.createFromJSON(json)
    });

	socket.on("trainer-exercise-start", () => {
		console.log(logTag, "trainer-exercise-start");
	});

	socket.on("trainer-exercise-stop", () => {
		console.log(logTag, "trainer-exercise-stop");
	});

	socket.on("patient-load-stopped", (arg) => {
		/** @type {PatientLoadNotRunning} */
		const patientLoad = JSON.parse(arg);
		console.log(logTag, "patient-load-stopped", patientLoad);
	});

	socket.on("patient-load-running", (arg) => {
		/** @type {PatientLoadRunning} */
		const patientLoad = JSON.parse(arg);
		console.log(logTag, "patient-load-running", patientLoad);
	});

	socket.on("patient-phase", (arg) => {
		/** @type {PatientPhaseChange} */
		const patientUpdate = JSON.parse(arg);
		console.log(logTag, "patient-phase", patientUpdate);
	});
}

/**
 * @param {TrainerLogin} login
 */
export function trainerLogin(login) {
    socket.emit("trainer-login", JSON.stringify(login));
}

export function trainerCreateExercise() {
    socket.emit("trainer-exercise-create");
}

export function trainerStartExercise() {
    socket.emit("trainer-exercise-start");
}

export function trainerExerciseStop() {
    socket.emit("trainer-exercise-stop");
}

/**
 * @param {PatientLogin} login
 */
export function patientLogin(login) {
    socket.emit("patient-login", JSON.stringify(login));
}

/**
 * @param {String} name
 */
export function addAction(name) {
    socket.emit("patient-action-add", JSON.stringify({exerciseCode: name}));
}

export const serverEvents = {
    trainerExerciseCreate: "trainer-exercise-create",
    trainerExerciseStart: "trainer-exercise-start",
    trainerExerciseStop: "trainer-exercise-stop",
    patientLoadNotRunning: "patient-load-stopped",
    patientLoadRunning: "patient-load-running",
    patientPhaseChange: "patient-phase",
}