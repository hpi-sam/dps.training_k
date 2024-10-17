import {defineStore} from 'pinia'
import type {AvailableAction, AvailableMaterial, AvailablePatient, Availables} from "@/sockets/MessageData"

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
		getActionCategories: (state) => {
			return [...new Set(state.actions.map((action) => action.actionCategory))]
		},
	},
	actions: {
		loadAvailableActions(json: AvailableAction[]) {
			this.actions = json
		},
		loadAvailablePatients(json: AvailablePatient[]) {
			this.patients = json
		},
		loadAvailableMaterials(json: AvailableMaterial[]) {
			this.material = json
		}
	}
})