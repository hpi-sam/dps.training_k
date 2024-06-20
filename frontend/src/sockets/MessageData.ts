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
	areaId?: number
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
	resourceAssignments: ResourceAssignment[]
	actions: Action[]
	injuries: Injury[]
	speed: number
	actionCheck: ActionCheck
	relocatingInfo: string
	timeUntilBack: number
}

interface Exercise {
	exerciseId: string
	status: string
	speed: number
	areas: Area[]
}

interface Area {
	areaId: number
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

interface ResourceAssignments {
	resourceAssignments: ResourceAssignment[]
}

interface ResourceAssignment {
	areaId: number
	personnel: PersonnelAssignments[]
	material: MaterialAssignments[]
}

interface PersonnelAssignments {
	personnelId: number
	patientId: string
}

interface MaterialAssignments {
	materialId: number
	patientId: string
}

interface Log {
	log: LogEntry[]
}

interface LogEntry {
	logId: number
	logMessage: string
	logTime: Date
	areaId: number
	patientId: string
	personnelIds: number[]
	materialNames: string[]
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

interface ActionCheck {
	actionName: string
	applicationDuration: number
	effectDuration: number
	personnel: CheckPersonnel[]
	material: CheckMaterial[]
	labDevices: CheckLabDevice[]
	requiredActions: RequiredActions
	prohibitedActions: string[]
}

interface RequiredActions {
	singleActions: string[]
	actionGroups: ActionGroup[]
}

interface ActionGroup {
	groupName: string
	actions: string[]
}

interface CheckPersonnel {
	name: string
	available: number
	assigned: number
	needed: number
}

interface CheckMaterial {
	name: string
	available: number
	assigned: number
	needed: number
}

interface CheckLabDevice {
	name: string
	available: number
	needed: number
}

interface PatientEditor {
	code: number
	firstState: number
	patientName: string
	triage: string
	personalDetails: string
	injury: string
	biometrics: string
	mobility: string
	preexistingIllnesses: string
	permanentMedication: string
	currentCaseHistory: string
	pretreatment: string
}

interface PatientState {
	id: number
	nodeId: string
	nextTransition: number
	airway: string
	breathing: string
	circulation: string
	consciousness: string
	psyche: string
	pupils: string
	skin: string
}

interface Transition {
	id: number
	nodeId: string
	firstCondition: number
	nextStates: number[]
}
