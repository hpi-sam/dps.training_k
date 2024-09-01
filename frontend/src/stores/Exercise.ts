import {defineStore} from 'pinia'

export const useExerciseStore = defineStore('exercise', {
	state: (): Exercise => ({
		exerciseId: "",
		status: ExerciseStatus.RUNNING,
		speed: 1,
		areas: [],
	}),
	getters: {
		getExerciseId: (state) => state.exerciseId,
		getArea: (state) => {
			return (areaId: number): Area | null => {
				return state.areas?.find(area => area.areaId === areaId) ?? null
			}
		},
		getAreaOfPatient: (state) => {
			return (patientId: string): Area | null => {
				return state.areas?.find(area =>
					area.patients.some(patient => patient.patientId === patientId)
				) ?? null
			}
		},
		getAreaIds: (state) => {
			return state.areas?.map(area => area.areaId) ?? []
		},
		getAreaName: (state) => {
			return (areaId: number): string | null => {
				const area = state.areas?.find(area => area.areaId === areaId)
				return area?.areaName ?? null
			}
		},
		getPatient: (state) => {
			return (patientId: string): Patient | null => {
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
		getMaterial: (state) => {
			return (materialId: number): Material | null => {
				return state.areas?.find(area =>
					area.material.find(material => material.materialId === materialId)
				)?.material?.find(material => material.materialId === materialId) ?? null
			}
		},
		getPersonnelOfArea: (state) => {
			return (areaId: number): Personnel[] | null => {
				const area = state.areas?.find(area => area.areaId === areaId)
				return area?.personnel ?? null
			}
		},
		getMaterialOfArea: (state) => {
			return (areaId: number): Material[] | null => {
				const area = state.areas?.find(area => area.areaId === areaId)
				return area?.material ?? null
			}
		}
	},
	actions: {
		createFromJSON(json: Exercise) {
			this.exerciseId = json.exerciseId
			this.areas = json.areas
		},
	}
})