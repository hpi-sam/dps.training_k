import {type ContinuousFunctionName, ContinuousVariableName} from "@/enums"

export interface MessageData {
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
	continuousState?: ContinuousState
	logEntries?: LogEntry[]
	availablePatients: AvailablePatient[]
	availableActions: AvailableAction[]
	availableMaterials: AvailableMaterial[]
	actionDeclinationReason?: string
	resourceAssignments: ResourceAssignment[]
	actions: Action[]
	injuries: Injury[]
	speed: number
	actionCheck?: ActionCheck
	relocatingInfo: string
	timeUntilBack: number
}

export interface ContinuousState {
	timeUntilPhaseChange: number
	continuousVariables: ContinuousVariable[]
}

export interface ContinuousStateInternal {
	timeUntilPhaseChange: number
	continuousVariables: ContinuousVariableInternal[]
}

export interface ContinuousVariable {
	name: ContinuousVariableName
	current: number
	target: number
	function: ContinuousFunctionName
}

export interface ContinuousVariableInternal {
	name: ContinuousVariableName
	xStart: number
	xCurrent: number
	xTarget: number
	tDelta: number
	function: ContinuousFunctionName
}


export interface Exercise {
	exerciseId: string
	status: string
	speed: number
	areas: Area[]
}

export interface Area {
	areaId: number
	areaName: string
	patients: Patient[]
	personnel: Personnel[]
	material: Material[]
}

export interface Patient {
	patientId: string
	patientName: string
	code: number
	triage: string
}

export interface Personnel {
	personnelId: number
	personnelName: string
}

export interface Material {
	materialId: number
	materialName: string
	materialType: string
}

export interface State {
	phaseNumber: number
	airway: string
	breathing: string
	circulation: string
	consciousness: string
	pupils: string
	psyche: string
	skin: string
}

export interface Availables {
	actions: AvailableAction[],
	patients: AvailablePatient[],
	material: AvailableMaterial[],
}

export interface AvailableAction {
	actionName: string
	actionCategory: string
}

export interface AvailablePatient {
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

export interface AvailableMaterial {
	materialName: string
	materialType: string
}

export interface ResourceAssignments {
	resourceAssignments: ResourceAssignment[]
}

export interface ResourceAssignment {
	areaId: number
	personnel: PersonnelAssignments[]
	material: MaterialAssignments[]
}

export interface PersonnelAssignments {
	personnelId: number
	patientId: string
}

export interface MaterialAssignments {
	materialId: number
	patientId: string
}

export interface Log {
	log: LogEntry[]
}

export interface LogEntry {
	logId: number
	logMessage: string
	logTime: Date
	areaId: number
	patientId: string
	personnelIds: number[]
	materialNames: string[]
}

export interface ActionOverview {
	actions: Action[]
	timersRunning: boolean
}

export interface Action {
	actionId: number
	orderId: number
	actionName: string
	actionStatus: string
	timeUntilCompletion: number
	actionResult: string
}

export interface VisibleInjuries {
	injuries: Injury[]
}

export interface Injury {
	injuryId: string
	injuryType: string
	position: string
}

export interface ActionCheck {
	actionName: string
	applicationDuration: number
	effectDuration: number
	personnel: CheckPersonnel[]
	material: CheckMaterial[]
	labDevices: CheckLabDevice[]
	requiredActions: RequiredActions
	prohibitiveActions: string[]
}

export interface RequiredActions {
	singleActions: string[]
	actionGroups: ActionGroup[]
}

export interface ActionGroup {
	groupName: string
	actions: string[]
}

export interface CheckPersonnel {
	name: string
	available: number
	assigned: number
	needed: number
}

export interface CheckMaterial {
	name: string
	available: number
	assigned: number
	needed: number
}

export interface CheckLabDevice {
	name: string
	available: number
	needed: number
}