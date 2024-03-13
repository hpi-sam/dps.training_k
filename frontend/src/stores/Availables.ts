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
			this.actions = json.actions
		},
		loadAvailablePatients(json: AvailablePatients) {
			console.log("AvailablePatients: "+JSON.stringify(json))
			this.patients = json.availablePatients
		},
		loadAvailableMaterial(json: AvailableMaterial) {
			this.material = json.material
		}
	}
})