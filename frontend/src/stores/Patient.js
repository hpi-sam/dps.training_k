import {defineStore} from "pinia"

export const usePatientStore = defineStore('patient', {
	state: () => ({
		token: '',
		patientCode: '',
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