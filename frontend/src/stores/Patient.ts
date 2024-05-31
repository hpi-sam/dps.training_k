import {defineStore} from "pinia"
import {useExerciseStore} from "@/stores/Exercise"
import {useAvailablesStore} from "./Availables"

export const usePatientStore = defineStore('patient', {
	state: () => ({
		token: '',
		patientId: '',
		code: Number.NEGATIVE_INFINITY,
		patientName: '',
		triage: '-',
		areaId: Number.NEGATIVE_INFINITY,
		airway: '',
		breathing: '',
		circulation: '',
		consciousness: '',
		psyche: '',
		pupils: '',
		skin: '',
		personalDetails: '', // currently unused - might be later configurable with birthday and address
		injury: '',
		biometrics: '',
		mobility: '',
		preexistingIllnesses: '',
		permanentMedication: '',
		currentCaseHistory: '',
		pretreatment: '',
	}),
	actions: {
		loadStatusFromJSON(state: State) {
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
			this.areaId = exerciseStore.getAreaOfPatient(this.patientId)?.areaId || Number.NEGATIVE_INFINITY
			this.triage = exerciseStore.getPatient(this.patientId)?.triage || '-'

			if (useAvailablesStore().getPatient(this.code)) this.initializePatientFromAvailablePatients()
		},
		initializePatientFromAvailablePatients() {
			const availablesStore = useAvailablesStore()
			this.injury = availablesStore.getPatient(this.code)?.injury || ''
			this.biometrics = availablesStore.getPatient(this.code)?.biometrics || ''
			this.mobility = availablesStore.getPatient(this.code)?.mobility || ''
			this.preexistingIllnesses = availablesStore.getPatient(this.code)?.preexistingIllnesses || ''
			this.permanentMedication = availablesStore.getPatient(this.code)?.permanentMedication || ''
			this.currentCaseHistory = availablesStore.getPatient(this.code)?.currentCaseHistory || ''
			this.pretreatment = availablesStore.getPatient(this.code)?.pretreatment || ''
		}
	}
})