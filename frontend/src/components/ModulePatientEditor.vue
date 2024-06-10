<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createEditor as createPatientEditor } from '@/rete/patient'
import { usePatientEditorStore } from '@/stores/patienteditor/PatientEditor'
import { usePatientStateStore } from '@/stores/patienteditor/PatientState'
import { useTransitionStore } from '@/stores/patienteditor/Transition'

const rete = ref(null)

  onMounted(async () => {
    const patientEditorStore = usePatientEditorStore()
    const patientStateStore = usePatientStateStore()
    const transitionStore = useTransitionStore()

    patientStateStore.addPatientState(
      {
        id: 1,
        nextTransition: 1,
        airway: 'open',
        breathing: 'normal',
        circulation: 'normal',
        consciousness: 'awake',
        psyche: 'normal',
        pupils: 'normal',
        skin: 'normal'
      }
    )

    patientStateStore.addPatientState(
      {
        id: 2,
        nextTransition: 2,
        airway: 'open',
        breathing: 'normal',
        circulation: 'normal',
        consciousness: 'awake',
        psyche: 'normal',
        pupils: 'normal',
        skin: 'normal'
      }
    )

    patientStateStore.addPatientState(
      {
        id: 3,
        nextTransition: Number.NEGATIVE_INFINITY,
        airway: 'open',
        breathing: 'normal',
        circulation: 'normal',
        consciousness: 'awake',
        psyche: 'normal',
        pupils: 'normal',
        skin: 'normal'
      }
    )

    transitionStore.addTransition(
      {
        id: 1,
        firstCondition: Number.NEGATIVE_INFINITY,
        nextStates: [2]
      }
    )

    transitionStore.addTransition(
      {
        id: 2,
        firstCondition: Number.NEGATIVE_INFINITY,
        nextStates: [3]
      }
    )

    await createPatientEditor(rete.value as HTMLElement, patientEditorStore, patientStateStore, transitionStore)
  })
</script>

<template>
	<main ref="rete" class="rete" />
</template>

<style scoped>
.rete {
  position: relative;
  height: 90vh;
  font-size: 1rem;
  background: white;
  text-align: left;
  line-height: 1;
}
</style>
