import {parentPort, workerData} from "worker_threads";
import now from "performance-now";
import {SocketTrainer} from "./sockets/SocketTrainer.js"
import {SocketPatient} from "./sockets/SocketPatient.js";
import {connectPatient, connectTrainer} from "./setupHelper.js";

const phaseLength = 30000 / 10

const socketTrainer = new SocketTrainer('http://localhost/ws/trainer/?token=')
const socketPatient = new SocketPatient('http://localhost/ws/patient/?token=')
let exerciseId, areaId, patientId

async function simulate(userIndex) {
	const trainerName = `testuser${crypto.randomUUID()}`

	try {
		await connectTrainer(socketTrainer, trainerName)
		await prepareExercise()
		await connectPatient(socketPatient, exerciseId, patientId)

		await new Promise(resolve => {
			socketTrainer.exerciseStart(() => {
				resolve()
			})
		})

		let responseTime = 0
		for (let i = 0; i < 5; i++) {
			let startTime = now();
			await new Promise(resolve => {
				socketPatient.addStateCb(() => {
					resolve()
				})
			})
			let endTime = now();
			responseTime += (endTime - startTime) - phaseLength
		}

		socketPatient.close()
		socketTrainer.close()

		parentPort.postMessage({
			userIndex,
			responseTime: responseTime / 5,
			success: true
		});
		parentPort.close()
	} catch (error) {
		parentPort.postMessage({
			userIndex,
			responseTime: now() - startTime,
			success: false,
			error: error.message
		});
	}
	parentPort.close()
}

async function prepareExercise() {
	await new Promise(resolve => {
		socketTrainer.exerciseCreate(exercise => {
			exerciseId = exercise.exerciseId
			resolve()
		})
	})

	await new Promise(resolve => {
		socketTrainer.areaAdd(exercise => {
			areaId = exercise.areas[0].areaId
			resolve(true)
		})
	})

	await new Promise(resolve => {
		socketTrainer.patientAdd(areaId, "", 1013, exercise => {
			patientId = exercise.areas[0].patients[0].patientId
			resolve()
		})
	})
}

simulate(workerData.userIndex);