import {defineStore} from 'pinia'

export const useExerciseStore = defineStore('exercise', {
	state: (): Exercise => ({
		exerciseId: "",
		areas: [],
	}),
	getters: {
		getExerciseCode: (state) => state.exerciseId,
		getArea: (state) => {
			return (areaName: string): Area | null => {
				return state.areas?.find(area => area.areaName === areaName) ?? null
			}
		},
		getAreaOfPatient: (state) => {
			return (patientId: number): Area | null => {
				return state.areas?.find(area =>
					area.patients.some(patient => patient.patientId === patientId)
				) ?? null
			}
		},
		getPatient: (state) => {
			return (patientId: number): Patient | null => {
				return state.areas?.find(area =>
					area.patients.find(patient => patient.patientId === patientId)
				)?.patients?.find(patient => patient.patientId === patientId) ?? null
			}
		},
		getPersonnel: (state) => {
			return (personnelId: number): Personnel | null => {
				return state.areas?.find(area =>
					area.personnel.find(personnel => personnel.personnelId === personnelId)
				)?.personnel?.find(personnel => personnel.personnelId === personnelId) ?? null
			}
		},
		getPersonnelOfArea: (state) => {
			return (areaName: string): Personnel[] => {
				let personnelList: Personnel[] = []
				state.areas.forEach((area) => {
					if (area.areaName == areaName) personnelList = area.personnel
				})
				return personnelList
			}
		},
		getMaterialOfArea: (state) => {
			return (areaName: string): Material[] => {
				let materialList: Material[] = []
				state.areas.forEach((area) => {
					if (area.areaName == areaName) materialList = area.material
				})
				return materialList
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