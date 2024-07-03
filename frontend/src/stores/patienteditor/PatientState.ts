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
    },
    exportToCSV() {
      const csv = this.patientStates.map(patientState => {
        const values = [
          patientState.id,
          patientState.nextTransition,
          patientState.airway,
          patientState.breathingRate,
          patientState.oxygenSaturation,
          patientState.breathing,
          patientState.breathingSound,
          patientState.breathingLoudness,
          patientState.heartRate,
          patientState.pulsePalpable,
          patientState.rivaRocci,
          patientState.consciousness,
          patientState.pupils,
          patientState.psyche,
          patientState.skinFining,
          patientState.skinDiscoloration,
          patientState.bgaOxy,
          patientState.bgaSbh,
          patientState.hb,
          patientState.bz,
          patientState.clotting,
          patientState.liver,
          patientState.kidney,
          patientState.infarct,
          patientState.lactate,
          patientState.extremities,
          patientState.thorax,
          patientState.trauma,
          patientState.ultraschall,
          patientState.ekg,
          patientState.zvd
        ]
        return values.join(',')
      }).join('\n')
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'patient-states.csv'
      a.click()
      URL.revokeObjectURL(url)
    }
  }
})