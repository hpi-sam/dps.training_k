import {defineStore} from 'pinia'

export const useAvailablesStore = defineStore('availables', {
	state: (): Availables => ({
		actions: [],
		patients: [],
		material: [],
	}),
	actions: {
		loadAvailableActions(json: AvailableActions) {
			this.actions = json.actions
		},
		loadAvailablePatients(json: AvailablePatients) {
			this.patients = json.patients
		},
		loadAvailableMaterial(json: AvailableMaterial) {
			this.material = json.material
		}
	}
})