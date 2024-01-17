export function configureFrontendSocket(frontendSocket) {
    frontendSocket.on("trainer.login", (args) => {
        console.log(args);
        const {username, password} = JSON.parse(args);
        const message = username === "test" && password === "test" ? "true" : "false";
        frontendSocket.emit("trainer.login.response", message);
    });

    frontendSocket.on("patient.login", (args) => {
        console.log(args);
        const {exerciseCode, patientCode} = JSON.parse(args);
        const message = exerciseCode === "123" && patientCode === "123" ? "true" : "false";
        frontendSocket.emit("patient.login.response", message);
    });
}
