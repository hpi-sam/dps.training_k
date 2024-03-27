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
		}
	},
	actions: {
		loadAvailableActions(json: AvailableActions) {
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