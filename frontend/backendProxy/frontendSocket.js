import {Exercise} from "../src/model/Exercise.js";
import {Area} from "../src/model/Area.js";
import {Device} from "../src/model/Device.js";
import {Patient, PatientLoadNotRunning, PatientLoadRunning, PatientPhaseChange, PatientState} from "../src/model/Patient.js";
import {Personnel} from "../src/model/Personnel.js";

/**
 * All frontend listeners for responses or server-side mock events.
 * For server-side mock events, add a case in the switch statement in the listener for the "test-event" event.
 * These events can be triggered from frontend with send event test button.
 * @param {Socket} frontendSocket
 */
export function configureFrontendSocket(frontendSocket) {
    frontendSocket.on("test-event", (args) => {
        /** @type {String} */
        const event = JSON.parse(args);

        switch (event) {
            case "trainer-exercise-create":
                args = JSON.stringify(new Exercise(
                    "123",
                    [
                        new Area("Area 1", [
                            new Patient("Patient 1", "123", "123", "123"),
                            new Patient("Patient 2", "123", "123", "123"),
                        ], [
                            new Personnel("Personnel 1", "Doctor", "123"),
                            new Personnel("Personnel 2", "Nurse", "123"),
                        ], [
                            new Device("Device 1", "123"),
                            new Device("Device 2", "123"),
                        ]),
                        new Area("Area 2", [
                            new Patient("Patient 3", "123", "123", "123"),
                            new Patient("Patient 4", "123", "123", "123"),
                        ], [
                            new Personnel("Personnel 3", "Doctor", "123"),
                            new Personnel("Personnel 4", "Nurse", "123"),
                        ], [
                            new Device("Device 3", "123"),
                            new Device("Device 4", "123"),
                        ]),
                    ]
                ));
                break;
            case "patient-load-stopped":
                args = JSON.stringify(new PatientLoadNotRunning(
                    "123",
                    "Area 1",
                ));
                break;
            case "patient-load-running":
                args = JSON.stringify(new PatientLoadRunning(
                    "123",
                    "Area 1",
                    new PatientState(
                        "Airway",
                        "Breathing",
                        "Circulation",
                        "Consciousness",
                        "Pupils",
                        "Psyche",
                        "Skin",
                    ),
                ));
                break;
            case "patient-phase":
                args = JSON.stringify(new PatientPhaseChange(
                    "1",
                    new PatientState(
                        "Airway",
                        "Breathing",
                        "Circulation",
                        "Consciousness",
                        "Pupils",
                        "Psyche",
                        "Skin",
                    ),
                ));
                break;
            default:
                args = null;
                break;
        }

        frontendSocket.emit(event, args);
    });

    frontendSocket.on("trainer-login", (args) => {
        const {username, password} = JSON.parse(args);
        const message = username === "test" && password === "test" ? "true" : "false";
        frontendSocket.emit("trainer-login", message);
    });

    frontendSocket.on("patient-login", (args) => {
        const {exerciseCode, patientCode} = JSON.parse(args);
        const message = exerciseCode === "123" && patientCode === "123" ? "true" : "false";
        frontendSocket.emit("patient-login", message);
    });
}
