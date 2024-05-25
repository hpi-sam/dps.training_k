import {defineStore} from 'pinia'

export const useResourceAssignmentsStore = defineStore('resourceAssignments', {
	state: (): ResourceAssignments => ({
        resourceAssignments: []
	}),
    getters: {
        getResourceAssignmentsOfArea: (state) => {
            return (areaId: number) : ResourceAssignment | null => {
                let foundResourceAssignment = null
                console.log('state for getResourceAssignmentsOfArea', state)
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