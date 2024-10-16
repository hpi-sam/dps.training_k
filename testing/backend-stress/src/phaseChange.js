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

		let responseTime_total = 0, responseTime_base = 0, responseTime_cv = 0
		for (let i = 0; i < 5; i++) {
			let endTime_base, endTime_cv
			let startTime = now();
			const statePromise = new Promise(resolve => {
				socketPatient.addStateCb(() => {
					resolve()
					endTime_base = now()
				})
			})
			const continuousPromise = new Promise(resolve => {
				socketPatient.addContinuousVariableCb(() => {
					resolve()
					endTime_cv = now()
				})
			})
			await Promise.all([statePromise, continuousPromise])
			let endTime_total = now();
			responseTime_total += (endTime_total - startTime) - phaseLength
			responseTime_base += (endTime_base - startTime) - phaseLength
			responseTime_cv += (endTime_cv - startTime) - phaseLength
		}

		socketPatient.close()
		socketTrainer.close()

		parentPort.postMessage({
			userIndex,
			responseTime_total: responseTime_total / 5,
			responseTime_base: responseTime_base / 5,
			responseTime_cv: responseTime_cv / 5,
			success: true
		});
		parentPort.close()
	} catch (error) {
		parentPort.postMessage({
			userIndex,
			responseTime_total: 0,
			responseTime_base: 0,
			responseTime_cv: 0,
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