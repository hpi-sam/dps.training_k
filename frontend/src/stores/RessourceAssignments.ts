import {defineStore} from 'pinia'

export const useRessourceAssignmentsStore = defineStore('ressourceAssignments', {
	state: (): RessourceAssignments => ({
        ressourceAssignments: []
	}),
    getters: {
        getRessourceAssignmentsOfArea: (state) => {
            return (areaName: string) : RessourceAssignment | null => {
                let foundRessourceAssignment = null
                state.ressourceAssignments.forEach((ressourceAssignment) => {
                    if (ressourceAssignment.areaName === areaName) {
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