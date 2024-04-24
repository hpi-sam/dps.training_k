import {defineStore} from 'pinia'

export const useAvailablesStore = defineStore('availables', {
	state: (): Availables => ({
		actions: [],
		patients: [],
		material: [],
	}),
	getters: {
		getPatient: (state) => {
			return (code: number): AvailablePatient | null => {
				let foundPatient: AvailablePatient | null = null
				state.patients.forEach((patient) => {
					if (patient.code == code) foundPatient = patient
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
			this.actions = json.availableActions
		},
		loadAvailablePatients(json: AvailablePatient[]) {
			this.patients = json
		},
		loadAvailableMaterial(json: AvailableMaterialList) {
			this.material = json.availableMaterialList
		}
	}
})