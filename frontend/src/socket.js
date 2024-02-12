import {reactive} from "vue";
import {io} from "socket.io-client";
import {useExerciseStore} from "./stores/Exercise.js";
import {setModule, showErrorToast, showWarningToast} from "@/App.vue";
import {setLeftScreen as moduleTrainerSetLeftScreen, setRightScreen as moduleTrainerSetRightScreen} from "@/components/ModuleTrainer.vue"

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
		if (bool) {
			setModule('ModuleTrainer')
		} else {
			showErrorToast("Fehler: falscher Nutzername oder falsches Passwort")
		}
	});

	socket.on("patient-login", (arg) => {
		/** @type {boolean} */
		const bool = JSON.parse(arg);
		if (bool) {
			setModule('ModulePatient')
		} else {
			showErrorToast("Fehler: Übung oder Patient existiert nicht")
		}
	});

	socket.on("trainer-exercise-create", (arg) => {
		if (!arg) {
			showErrorToast("Fehler: Übung konnte nicht erstellt werden")
		}
		const json = JSON.parse(arg)
		exerciseStore.createFromJSON(json)
		moduleTrainerSetLeftScreen('ScreenExerciseCreation')
		moduleTrainerSetRightScreen('ScreenResourceCreation')
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
export function trainerLogin(username, password) {
	socket.emit("trainer-login", JSON.stringify({username: username, password: password}));
}

export function trainerExerciseCreate() {
	socket.emit("trainer-exercise-create");
}

export function trainerExerciseStart() {
	socket.emit("trainer-exercise-start");
}

export function trainerExerciseStop() {
	socket.emit("trainer-exercise-stop");
}

/**
 * @param {PatientLogin} login
 */
export function patientLogin(exerciseCode, patientCode) {
	socket.emit("patient-login", JSON.stringify({exerciseCode: exerciseCode, patientCode: patientCode}));
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