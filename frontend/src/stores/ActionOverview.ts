import {defineStore} from 'pinia'

export const useActionOverviewStore = defineStore('actionOverview', {
	state: (): ActionOverview => ({
		actions: [],
		timersRunning: false
	}),
	actions: {
		loadActions(json: Action[]) {
			console.log('loadActions1 ', json)
			this.actions = json
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