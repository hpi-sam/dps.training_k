import {defineStore} from 'pinia'

export const useActionCheckStore = defineStore('actionCheck', {
	state: (): ActionCheck => ({
        actionName: "",
		applicationDuration: 0,
        effectDuration: 0,
        personnel: [] as CheckPersonnel[],
        material: [] as CheckMaterial[],
        labDevices: [] as CheckLabDevice[],
        requiredActions: {} as RequiredActions,
        prohibitedActions: [] as string[],
	}),
	actions: {
        loadActionCheck(actionCheck: ActionCheck) {
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