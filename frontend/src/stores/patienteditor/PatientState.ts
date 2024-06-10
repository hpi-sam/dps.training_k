import { defineStore } from 'pinia'

export const usePatientStateStore = defineStore('patient-state', {
  state: (): { patientStates: Record<number, PatientState> } => ({
    patientStates: {},
  }),
  getters: {
    getNextTransition: (state) => Object.values(state.patientStates).map(patientState => patientState.nextTransition),
  },
  actions: {
    addPatientState(patientState: PatientState) {
      this.patientStates[patientState.id] = patientState
    },
    removePatientState(id: number) {
      delete this.patientStates[id]
    },
    updatePatientState(id: number, newPatientState: PatientState) {
      this.patientStates[id] = newPatientState
    },
  }
})