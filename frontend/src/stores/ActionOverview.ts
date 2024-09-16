import {defineStore} from 'pinia'
import type {Action, ActionOverview} from "@/sockets/MessageData"

export const useActionOverviewStore = defineStore('actionOverview', {
	state: (): ActionOverview => ({
		actions: [],
		timersRunning: false
	}),
	actions: {
		loadActions(json: Action[]) {
			this.actions = json.sort((a, b) => b.orderId - a.orderId)
		},
		decreaseTimeForRunningActions() {
			this.actions = this.actions.map(action => {
				if ((action.actionStatus === 'IP' || action.actionStatus === 'IE') && action.timeUntilCompletion > 0) {
					return {...action, timeUntilCompletion: action.timeUntilCompletion - 1}
				}
				return action
			})
		},
		startUpdatingTimers() {
			if (this.timersRunning) return
			this.timersRunning = true
			setInterval(() => {
				this.decreaseTimeForRunningActions()
			}, 1000)
		}
	}
})