// eslint-disable-next-line @typescript-eslint/no-unused-vars
interface MessageData {
	messageType: string
	message?: string
	patientName?: string
	areaName?: string
	token?: string
	triage?: string
	name?: string
	exercise?: Exercise
	state?: State
}

interface Exercise {
	exerciseCode: number
	areas: Area[]
}

interface Area {
	name: string
	patients: Patient[]
	personnel: Personnel[]
	devices: Device[]
}

interface Patient {
	name: string
	patientCode: string
	patientId: number
	patientDatabaseId: number
}

interface Personnel {
	name: string
	role: string
	personnelDatabaseId: number
}

interface Device {
	name: string
	deviceDatabaseId: number
}

interface State {
	phaseNumber: number
	airway: string
	breathing: string
	circulation: string
	consciousness: string
	pupils: string
	psyche: string
	skin: string
}
