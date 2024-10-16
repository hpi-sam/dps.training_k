import {parentPort, workerData} from "worker_threads";
import now from "performance-now";
import {SocketTrainer} from "./sockets/SocketTrainer.js"
import {SocketPatient} from "./sockets/SocketPatient.js";
import {connectPatient, connectTrainer} from "./setupHelper.js";

const actionName = "Turniquet"
const actionTime = 15000 / 10

const socketTrainer = new SocketTrainer('http://localhost/ws/trainer/?token=')
const socketPatient = new SocketPatient('http://localhost/ws/patient/?token=')
let exerciseId, areaId, patientId, personnelId

async function simulate(userIndex) {
	const trainerName = `testuser${crypto.randomUUID()}`

	try {
		await connectTrainer(socketTrainer, trainerName)
		await prepareExercise()
		await connectPatient(socketPatient, exerciseId, patientId)

		await new Promise(resolve => {
			socketPatient.assignPersonnel(personnelId, () => resolve())
		})

		let endTime_base, endTime_cv
		const startTime = now();
		const actionPromise = new Promise(resolve => {
			socketPatient.actionAdd(actionName, confirmed => {
				if (!confirmed) throw Error("action declined")
			}, () => {
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

		await Promise.all([actionPromise, continuousPromise])
		const endTime_total = now();

		socketPatient.close()
		socketTrainer.close()

		parentPort.postMessage({
			userIndex,
			responseTime_total: (endTime_total - startTime) - actionTime, // subtract execution time of action
			responseTime_base: (endTime_base - startTime) - actionTime, // subtract execution time of action
			responseTime_cv: (endTime_cv - startTime) - actionTime, // subtract execution time of action
			success: true
		});
		parentPort.close()
	} catch (error) {
		parentPort.postMessage({
			userIndex,
			responseTime: 0,
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
		socketTrainer.personnelAdd(areaId, "", exercise => {
			personnelId = exercise.areas[0].personnel[0].personnelId
			resolve()
		})
	})

	await new Promise(resolve => {
		socketTrainer.exerciseStart(() => resolve())
	})
}

simulate(workerData.userIndex);