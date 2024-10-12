import { parentPort, workerData } from "worker_threads";
import axios from "axios";
import now from "performance-now";
import {SocketTrainer} from "./sockets/SocketTrainer.js"
// import {NUM_TRAINER_PER_EXERCISE} from "./main.js";

async function simulateExercise(userIndex) {
	const trainerName = `testuser${crypto.randomUUID()}`

	const startTime = now();

	try {
		const response = await axios.post(`https://klinik-dps.de/api/trainer/login`, {
			username: trainerName,
			password: 'password123'
		});
		const token = response.data.token;

		const socketTrainer = new SocketTrainer('https://klinik-dps.de/ws/trainer/?token=')

		await new Promise(resolve => {
			socketTrainer.connect(token, response => resolve(response));
		});

		socketTrainer.testPassthrough((message) => {console.log(message)})

		const endTime = now();

		parentPort.postMessage({
			userIndex,
			responseTime: endTime - startTime,
			success: true
		});
	} catch (error) {
		parentPort.postMessage({
			userIndex,
			responseTime: now() - startTime,
			success: false,
			error: error.message
		});
	}
}

simulateExercise(workerData.userIndex);