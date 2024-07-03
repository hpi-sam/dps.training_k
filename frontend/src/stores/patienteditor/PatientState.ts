import { defineStore } from 'pinia'

export const usePatientStateStore = defineStore('patient-state', {
  state: (): PatientStates => ({
    patientStates: [],
  }),
  getters: {
    getNextTransition: (state) => state.patientStates.map(patientState => patientState.nextTransition),
    getPatientStateById: (state) => {
      return (id: number) => state.patientStates.find(patientState => patientState.id === id)
    },
    getPatientStateByNodeId: (state) => {
      return (nodeId: string) => state.patientStates.find(patientState => patientState.nodeId === nodeId)
    }
  },
  actions: {
    addPatientState(patientState: PatientState) {
      this.patientStates.push(patientState)
    },
    removePatientState(id: number) {
      this.patientStates.filter(patientState => patientState.id !== id)
    },
    updatePatientState(id: number, newPatientState: PatientState) {
      const index = this.patientStates.findIndex(patientState => patientState.id === id)
      this.patientStates[index] = newPatientState
    },
    clear() {
      this.patientStates = []
    }
  }
})