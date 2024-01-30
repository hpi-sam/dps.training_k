import { defineStore } from "pinia"

export const usePatientStateStore = defineStore('patientState', {
    state: () => ({
        phaseNumer: 0,
        airway: '',
        breathing: '',
        circulation: '',
        consciousness: '',
        pupils: '',
        psyche: '',
        skin: ''
    })
})