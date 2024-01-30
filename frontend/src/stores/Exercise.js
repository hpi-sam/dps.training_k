import {defineStore} from 'pinia'
import { useAreaStore } from './Area'

export const useExerciseStore = defineStore('exercise', {
    state: () => ({
        exerciseCode: '',
        areas: []
    }),
    getters: {
        getArea(patientCode){
            this.areas.array.forEach(area => {
                if(area.patients.find((p) => p.patients.patientCode == patientCode)){
                    return area
                }
            })
            return null
        },
        getPatient(patientCode){
            const area = this.getArea(patientCode)
            if(!area) return null
            return area.patients.find((p) => p.patients.patientCode == patientCode)
        }
    },
    actions: {
        createAreaStore(){
            const newAreaStore = useAreaStore()
            this.areas.push(newAreaStore)
        },
        createFromJSON(json){
            this.exerciseCode = json.exerciseCode
            this.areas = json.areas
        }
    }
})