import {defineStore} from 'pinia'
import type {Log, LogEntry} from "@/sockets/MessageData"

export const useLogStore = defineStore('log', {
	state: (): Log => ({
		log: []
	}),
	getters: {
		getLogEntry: (state) => {
			return (logId: number): LogEntry | null => {
				let foundLogEntry: LogEntry | null = null
				state.log.forEach((logEntry) => {
					if (logEntry.logId == logId) foundLogEntry = logEntry
				})
				return foundLogEntry
			}
		}
	},
	actions: {
		sortLogByLogTime() {
			this.log = this.log.sort((a, b) => {
				return new Date(b.logTime).getTime() - new Date(a.logTime).getTime()
			})
		},
		addLogEntries(logEntries: LogEntry[]) {
			this.log.push(...logEntries)
			this.sortLogByLogTime()
		}
	}
})