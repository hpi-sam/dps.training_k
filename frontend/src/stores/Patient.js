import { defineStore } from "pinia"

export const usePatientStore = defineStore('patient', {
    state: () => ({
        name: '',
        patientCode: '',
        patientId: '',
        patientDatabaseId: ''
    })
})

export const usePatientLoginStore = defineStore('patientLogin', {
    state: () => ({
        exerciseCode: '',
        patientCode: ''
    }),
    getters: {
        isCorrect: (state) => {
            return state.exerciseCode === "123" && state.patientCode === "123"
        }
    }
})

export const usePatientLoadNotRunningStore = defineStore('patientLoadNotRunning', {
    state: () => ({
        patientName: '',
        areaName: ''
    })
})

export const usePatientLoadRunningStore = defineStore('patientLoadRunning', {
    state: () => ({
        patientName: '',
        areaName: '',
        patientState: {}
    })
})

export const usePatientStateStore = defineStore('patientState', {
    state: () => ({
        airway: '',
        breathing: '',
        circulation: '',
        consciousness: '',
        pupils: '',
        psyche: '',
        skin: ''
    })
})

export const usePatientPhaseChangeStore = defineStore('patientPhaseChange', {
    state: ({
        phaseNumber: 0,
        patientState: {}
    })
})