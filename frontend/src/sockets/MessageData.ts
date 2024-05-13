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
	code?: number
	patientId?: string
	personnelName?: string
	personnelId?: number
	materialName?: string
	exercise?: Exercise
	state?: State
	logEntries?: LogEntry[]
	availablePatients: AvailablePatient[]
	availableActions: AvailableAction[]
	availableMaterials: AvailableMaterial[]
	actionDeclinationReason?: string
	ressourceAssignments: RessourceAssignments
	actions: Action[]
	injuries: Injury[]
	speed: number
}

interface Exercise {
	exerciseId: string
	status: string
	speed: number
	areas: Area[]
}

interface Area {
	areaName: string
	patients: Patient[]
	personnel: Personnel[]
	material: Material[]
}

interface Patient {
	patientId: string
	patientName: string
	code: number
	triage: string
}

interface Personnel {
	personnelId: number
	personnelName: string
}

interface Material {
	materialId: number
	materialName: string
	materialType: string
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

interface Availables {
	actions: AvailableAction[],
	patients: AvailablePatient[],
	material: AvailableMaterial[],
}

interface AvailableAction {
	actionName: string
	actionCategory: string
}

interface AvailablePatient {
	code: number
	personalDetails: string
	injury: string
	biometrics: string
	triage: string
	consecutiveUniqueNumber: number
	mobility: string
	preexistingIllnesses: string
	permanentMedication: string
	currentCaseHistory: string
	pretreatment: string
}

interface AvailableMaterial {
	materialName: string
	materialType: string
}

interface RessourceAssignments {
	ressourceAssignments: RessourceAssignment[]
}

interface RessourceAssignment {
	areaName: string
	personnel: PersonnelAssignments[]
	material: MaterialAssignments[]
}

interface PersonnelAssignments {
	personnelId: number
	personnelName: string
	patientId: string
}

interface MaterialAssignments {
	materialId: number
	materialName: string
	patientId: string
}

interface Log {
	log: LogEntry[]
}

interface LogEntry {
	logId: number
	logMessage: string
	logTime: Date
	areaName: string
	patientId: string
	personnelId: number
}

interface ActionOverview {
	actions: Action[]
	timersRunning: boolean
}

interface Action {
	actionId: number
	orderId: number
	actionName: string
	actionStatus: string
	timeUntilCompletion: number
	actionResult: string
}

interface VisibleInjuries {
	injuries: Injury[]
}

interface Injury {
	injuryId: string
	injuryType: string
	position: string
}