import {defineStore} from 'pinia'

export const useExerciseStore = defineStore('exercise', {
	state: (): Exercise => ({
		exerciseId: Number.NEGATIVE_INFINITY,
		areas: [],
	}),
	getters: {
		getExerciseCode: (state) => state.exerciseId,
		getArea: (state) => {
			return (areaName: string): Area | null => {
				let foundArea: Area | null = null
				state.areas.forEach((area) => {
					if (area.areaName == areaName) foundArea = area
				})
				return foundArea
			}
		},
		getAreaOfPatient: (state) => {
			return (patientId: number): Area | null => {
				let foundArea: Area | null = null
				state.areas.forEach((area) => {
					area.patients.forEach((patient) => {
						if (patient.patientId == patientId) foundArea = area
					})
				})
				return foundArea
			}
		},
		getPatient: (state) => {
			return (patientId: number): Patient | null => {
				let foundPatient: Patient | null = null
				state.areas.forEach((area) => {
					area.patients.forEach((patient) => {
						if (patient.patientId == patientId) foundPatient = patient
					})
				})
				return foundPatient
			}
		},
		getPersonnel: (state) => {
			return (personnelId: number): Personnel | null => {
				let foundPersonnel: Personnel | null = null
				state.areas.forEach((area) => {
					area.personnel.forEach((personnel) => {
						if (personnel.personnelId == personnelId) foundPersonnel = personnel
					})
				})
				return foundPersonnel
			}
		}
	},
	actions: {
		createFromJSON(json: Exercise) {
			this.exerciseId = json.exerciseId
			this.areas = json.areas
		}
	}
})