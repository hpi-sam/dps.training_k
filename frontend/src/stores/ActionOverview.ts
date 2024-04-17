import {defineStore} from 'pinia'

export const useActionOverviewStore = defineStore('actionOverview', {
	state: (): ActionOverview => ({
		actions: [],
		timersRunning: false
	}),
	actions: {
		loadActions(json: Action[]) {
			this.actions = json.sort((a, b) => a.orderId - b.orderId)
		},
		decreaseTimeForRunningActions() {
			this.actions = this.actions.map(action => {
				if (action.actionStatus === 'running' && action.timeUntilCompletion > 0) {
					return { ...action, timeUntilCompletion: action.timeUntilCompletion - 1 }
				}
			return action
			})
		},
		startUpdating() {
			if (this.timersRunning) return
			this.timersRunning = true
			setInterval(() => {
				this.decreaseTimeForRunningActions()
			}, 1000)
		}
	}
})