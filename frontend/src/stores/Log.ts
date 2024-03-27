import {defineStore} from 'pinia'

export const useLogStore = defineStore('log', {
	state: (): Log => ({
		log: []
	}),
	actions: {
        addLogEntries(logEntries: LogEntry[]) {
			console.log(logEntries)
			this.log.push(...logEntries)
        }
	}
})