import {defineStore} from 'pinia'

export const useRessourceAssignmentsStore = defineStore('ressourceAssignments', {
	state: (): RessourceAssignments => ({
        ressourceAssignments: []
	}),
    getters: {
        getRessourceAssignmentsOfArea: (state) => {
            return (areaId: number) : RessourceAssignment | null => {
                let foundRessourceAssignment = null
                state.ressourceAssignments.forEach((ressourceAssignment) => {
                    if (ressourceAssignment.areaId === areaId) {
                        foundRessourceAssignment = ressourceAssignment
                    }
                })
                return foundRessourceAssignment
            }
        }
    },
	actions: {
		setRessourceAssignments(json: RessourceAssignments) {
			this.ressourceAssignments = json.ressourceAssignments
		}
	}
})