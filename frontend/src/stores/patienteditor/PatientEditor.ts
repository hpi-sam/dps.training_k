import {defineStore} from 'pinia'

export const usePatientEditorStore = defineStore('patient-editor', {
	state: (): PatientEditor => ({
		code: Number.NEGATIVE_INFINITY,
        firstState: Number.NEGATIVE_INFINITY,
		patientName: '',
		triage: '-',
		personalDetails: '', // currently unused - might be later configurable with birthday and address
		injury: '',
		biometrics: '',
		mobility: '',
		preexistingIllnesses: '',
		permanentMedication: '',
		currentCaseHistory: '',
		pretreatment: '',
	}),
	getters: {
        getFirstState: (state) => state.firstState,
	}
})