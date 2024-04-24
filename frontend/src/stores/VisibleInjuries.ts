import { addInjury } from '@/components/widgets/PatientModel.vue'
import {defineStore} from 'pinia'

export const useVisibleInjuriesStore = defineStore('visibleInjuries', {
	state: (): VisibleInjuries => ({
		injuries: []
	}),
    actions: {
        loadVisibleInjuries(json: Injury[]) {
            this.injuries = json
            this.showVisibleInjuries()
        },
        showVisibleInjuries() {
            for (const injury of this.injuries) {
                addInjury(injury.injuryType, injury.position)
            }
        }
    }
})