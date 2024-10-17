import {defineStore} from 'pinia'
import type {ResourceAssignment, ResourceAssignments} from "@/sockets/MessageData"

export const useResourceAssignmentsStore = defineStore('resourceAssignments', {
	state: (): ResourceAssignments => ({
		resourceAssignments: []
	}),
	getters: {
		getResourceAssignmentsOfArea: (state) => {
			return (areaId: number): ResourceAssignment | null => {
				let foundResourceAssignment = null
				state.resourceAssignments.forEach((resourceAssignment) => {
					if (resourceAssignment.areaId === areaId) {
						foundResourceAssignment = resourceAssignment
					}
				})
				return foundResourceAssignment
			}
		}
	},
	actions: {
		setResourceAssignments(json: ResourceAssignment[]) {
			this.resourceAssignments = json
		}
	}
})