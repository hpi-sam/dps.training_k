import {defineStore} from 'pinia'

export const useAvailablesStore = defineStore('availables', {
	state: (): Availables => ({
		actions: [],
		patients: [],
		material: [],
	}),
	getters: {
		getPatient: (state) => {
			return (patientCode: number): AvailablePatient | null => {
				let foundPatient: AvailablePatient | null = null
				state.patients.forEach((patient) => {
					if (patient.patientCode == patientCode) foundPatient = patient
				})
				return foundPatient
			}
		},
		getActionTypes: (state) => {
			return [...new Set(state.actions.map((action) => action.actionType))]
		},
	},
	actions: {
		loadAvailableActions(json: AvailableActions) {
			console.log('Store: Available actions:', json.availableActions)
			this.actions = json.availableActions
		},
		loadAvailablePatients(json: AvailablePatients) {
			this.patients = json.availablePatients
		},
		loadAvailableMaterial(json: AvailableMaterialList) {
			this.material = json.availableMaterialList
		}
	}
})