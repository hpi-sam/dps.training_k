import {defineStore} from 'pinia';

export const useExerciseStore = defineStore('exercise', {
	state: (): Exercise => ({
		exerciseCode: 0,
		areas: [],
	}),
	getters: {
		getExerciseCode: (state) => state.exerciseCode,
		getArea: (state) => {
			return (patientCode: string): Area | null => {
				let foundArea: Area | null = null;
				state.areas.forEach((area) => {
					area.patients.forEach((patient) => {
						if (patient.patientCode == patientCode) foundArea = area
					})
				})
				return foundArea
			}
		},
	},
	actions: {
		createFromJSON(json: Exercise) {
			this.exerciseCode = json.exerciseCode
			this.areas = json.areas
			console.log(json)
		}
	}
})