import {defineStore} from "pinia"

export const usePatientStore = defineStore('patient', {
	state: () => ({
		token: '',
		patientCode: '',
		triage: '-',
		areaName: '',
        airway: '',
        breathing: '',
        circulation: '',
        consciousness: '',
		phaseNumer: 0,
        psyche: '',
        pupils: '',
        skin: ''
	}),
    actions: {
        loadStatusFromJSON(json){
            const state = json.state
			this.airway = state.airway
			this.breathing = state.breathing
			this.circulation = state.circulation
			this.consciousness = state.consciousness
			this.phaseNumer = state.phaseNumer
			this.psyche = state.psyche
			this.pupils = state.pupils
			this.skin = state.skin
        }
    }
})