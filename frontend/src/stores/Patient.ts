import {defineStore} from "pinia"
import {useExerciseStore} from "@/stores/Exercise"
import {useAvailablesStore} from "./Availables"

export const usePatientStore = defineStore('patient', {
	state: () => ({
		token: '',
		patientId: Number.NEGATIVE_INFINITY,
		code: Number.NEGATIVE_INFINITY,
		patientName: '',
		triage: '-',
		areaName: '',
		airway: '',
		breathing: '',
		circulation: '',
		consciousness: '',
		phaseNumber: 0,
		psyche: '',
		pupils: '',
		skin: '',
		injury: '',
		history: '',
		personalDetails: '',
		biometrics: ''
	}),
	actions: {
		loadStatusFromJSON(state: State) {
			this.phaseNumber = state.phaseNumber
			this.airway = state.airway
			this.breathing = state.breathing
			this.circulation = state.circulation
			this.consciousness = state.consciousness
			this.psyche = state.psyche
			this.pupils = state.pupils
			this.skin = state.skin
		},
		initializePatientFromExercise() {
			const exerciseStore = useExerciseStore()
			this.patientName = exerciseStore.getPatient(this.patientId)?.patientName || ''
			this.code = exerciseStore.getPatient(this.patientId)?.code || Number.NEGATIVE_INFINITY
			this.areaName = exerciseStore.getAreaOfPatient(this.patientId)?.areaName || ''
			this.triage = exerciseStore.getPatient(this.patientId)?.triage || '-'
		},
		initializePatientFromAvailablePatients() {
			const availablesStore = useAvailablesStore()
			this.injury = availablesStore.getPatient(this.patientCode)?.patientInjury || ''
			this.history = availablesStore.getPatient(this.patientCode)?.patientHistory || ''
			this.personalDetails = availablesStore.getPatient(this.patientCode)?.patientPersonalDetails || ''
			this.biometrics = availablesStore.getPatient(this.patientCode)?.patientBiometrics || ''
		}
	}
})