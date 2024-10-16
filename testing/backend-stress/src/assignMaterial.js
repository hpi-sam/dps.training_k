import { parentPort, workerData } from "worker_threads";
import now from "performance-now";
import {SocketTrainer} from "./sockets/SocketTrainer.js"
import {SocketPatient} from "./sockets/SocketPatient.js";
import {connectPatient, connectTrainer} from "./setupHelper.js";

const socketTrainer = new SocketTrainer('http://localhost/ws/trainer/?token=')
const socketPatient = new SocketPatient('http://localhost/ws/patient/?token=')
let exerciseId, areaId, patientId, materialId

const assignmentCycles = 50

async function simulate(userIndex) {
	const trainerName = `testuser${crypto.randomUUID()}`

	try {
		await connectTrainer(socketTrainer, trainerName)
		await prepareExercise()
		await connectPatient(socketPatient, exerciseId, patientId)

		let responseTime_total = 0, responseTime_base = 0, responseTime_cv = 0

		for (let i = 0; i < assignmentCycles; i++) {
			let endTime_base, endTime_cv
			let startTime = now();
			const assignmentPromise1 = new Promise(resolve => {
				socketPatient.assignMaterial(materialId, () => {
					resolve()
					endTime_base = now()
				})
			})
			const continuousPromise1 = new Promise(resolve => {
				socketPatient.addContinuousVariableCb(() => {
					resolve()
					endTime_cv = now()
				})
			})
			await Promise.all([assignmentPromise1, continuousPromise1])
			let endTime_total = now();
			responseTime_total += (endTime_total - startTime)
			responseTime_base += (endTime_base - startTime)
			responseTime_cv += (endTime_cv - startTime)

			startTime = now();
			const assignmentPromise2 = new Promise(resolve => {
				socketPatient.releaseMaterial(materialId, () => {
					resolve()
					endTime_base = now()
				})
			})
			const continuousPromise2 = new Promise(resolve => {
				socketPatient.addContinuousVariableCb(() => {
					resolve()
					endTime_cv = now()
				})
			})
			await Promise.all([assignmentPromise2, continuousPromise2])
			endTime_total = now();
			responseTime_total += (endTime_total - startTime)
			responseTime_base += (endTime_base - startTime)
			responseTime_cv += (endTime_cv - startTime)
		}


		socketPatient.close()
		socketTrainer.close()

		parentPort.postMessage({
			userIndex,
			responseTime_total: responseTime_total / (assignmentCycles*2),
			responseTime_base: responseTime_base / (assignmentCycles*2),
			responseTime_cv: responseTime_cv / (assignmentCycles*2),
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
		socketTrainer.patientAdd(areaId, "", 1001, exercise => {
			patientId = exercise.areas[0].patients[0].patientId
			resolve()
		})
	})

	await new Promise(resolve => {
		socketTrainer.materialAdd(areaId, "BZ-Messgerät", exercise => {
			materialId = exercise.areas[0].material[0].materialId
			resolve()
		})
	})

	await new Promise(resolve => {
		socketTrainer.exerciseStart(() => resolve())
	})
}

simulate(workerData.userIndex);