/* eslint-disable @typescript-eslint/no-unused-vars */
interface MessageData {
	messageType: string
	message?: string
	triage?: string
	actionName?: string
	patientInjury?: string
	patientHistory?: string
	patientPersonalDetails?: string
	patientBiometrics?: string
	areaName?: string
	patientName?: string
	patientCode?: number
	patientId?: number
	personnelName?: string
	personnelId?: number
	deviceName?: string
	deviceId?: number
	exercise?: Exercise
	state?: State
	logEntry?: LogEntry
	availablePatients: AvailablePatients
	availableActions: AvailableActions
	availableMaterial: AvailableMaterial
}

interface Exercise {
	exerciseId: number
	areas: Area[]
}

interface Area {
	areaName: string
	patients: Patient[]
	personnel: Personnel[]
	devices: Device[]
}

interface Patient {
	patientId: number
	patientName: string
	patientCode: number
}

interface Personnel {
	personnelId: number
	personnelName: string
}

interface Device {
	deviceId: number
	deviceName: string
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

interface LogEntry {
	logMessage: string
	logTime: Date
	areaName: string
	patientId: number
	personnelId: number
	deviceId: number
}

interface AvailablePatient {
	patientCode: number
	triage: string
	patientInjury: string
	patientHistory: string
	patientPersonalDetails: string
	patientBiometrics: string
}

interface Availables {
	actions: [],
	patients: AvailablePatient[],
	material: [],
}

interface AvailableActions {
	actions: [],
}

interface AvailablePatients {
	patients: AvailablePatient[],
}

interface AvailableMaterial {
	material: [],
}