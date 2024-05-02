import {defineStore} from 'pinia'

export const useActionCheckStore = defineStore('actionCheck', {
	state: (): ActionCheck => ({
        actionName: "",
		applicationDuration: 0,
        effectDuration: 0,
        personnel: [],
        material: [],
        labDevices: [],
        requiredActions: {} as RequiredActions,
        prohibitedActions: [],
	}),
	actions: {
        loadActionCheck(actionCheck: ActionCheck) {
            console.log("1: "+actionCheck)
            console.log("2: "+actionCheck.applicationDuration)
            this.actionName = actionCheck.actionName
            this.applicationDuration = actionCheck.applicationDuration
            this.effectDuration = actionCheck.effectDuration
            this.personnel = actionCheck.personnel
            this.material = actionCheck.material
            this.labDevices = actionCheck.labDevices
            this.requiredActions = actionCheck.requiredActions
            this.prohibitedActions = actionCheck.prohibitedActions
        }
	}
})