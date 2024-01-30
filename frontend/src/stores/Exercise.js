import {defineStore} from 'pinia'

export const useExerciseStore = defineStore('exercise', {
    state: () => ({
        exerciseCode: '',
        areas: []
    }),
    getters: {
        getExerciseCode: (state) => state.exerciseCode,
        getArea(state){
            return (patientCode) => {
                let foundArea = null
                state.areas.forEach(area => {
                    area.patients.forEach(patient => {
                        if(patient.patientCode == patientCode){
                            foundArea = area
                        }
                    })
                })
                return foundArea
            }
        },
        getPatient(state){
            return (patientCode) => {
                const area = state.getArea(patientCode)
                if(!area) return null
                let foundPatient = null
                area.patients.forEach(patient => {
                    if(patient.patientCode == patientCode){
                        foundPatient = patient
                    }
                })
                return foundPatient
            }
        },
    },
    actions: {
        createFromJSON(json){
            this.exerciseCode = json.exerciseCode
            this.areas = json.areas
            console.log(json)
        }
    }
})