import axios from "axios";

export async function connectTrainer(socketTrainer, trainerName) {
	const response = await axios.post(`http://localhost/api/trainer/login`, {
		username: trainerName,
		password: 'password123'
	})
	const token = response.data.token;

	await new Promise(resolve => {
		socketTrainer.connect(token, () => resolve())
	})
}

export async function connectPatient(socketPatient, exerciseId, patientId) {
	const response = await axios.post(`http://localhost/api/patient/access`, {
		exerciseId: exerciseId,
		patientId: patientId,
	})
	const token = response.data.token;

	await new Promise(resolve => {
		socketPatient.connect(token, () => resolve())
	})
}