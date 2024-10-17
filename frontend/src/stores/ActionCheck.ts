import {defineStore} from 'pinia'
import type {ActionCheck, CheckLabDevice, CheckMaterial, CheckPersonnel, RequiredActions} from "@/sockets/MessageData"

export const useActionCheckStore = defineStore('actionCheck', {
	state: (): ActionCheck => ({
		actionName: "",
		applicationDuration: 0,
		effectDuration: 0,
		personnel: [] as CheckPersonnel[],
		material: [] as CheckMaterial[],
		labDevices: [] as CheckLabDevice[],
		requiredActions: {} as RequiredActions,
		prohibitiveActions: [] as string[],
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
			this.prohibitiveActions = actionCheck.prohibitiveActions
		}
	}
})