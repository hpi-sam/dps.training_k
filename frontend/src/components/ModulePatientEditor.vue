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
        nodeId: '',
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
        nodeId: '',
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
        nodeId: '',
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
        nodeId: '',
        firstCondition: Number.NEGATIVE_INFINITY,
        nextStates: [2]
      }
    )

    transitionStore.addTransition(
      {
        id: 2,
        nodeId: '',
        firstCondition: Number.NEGATIVE_INFINITY,
        nextStates: [3]
      }
    )

    if (rete.value) {
      await createPatientEditor(rete.value as HTMLElement, patientEditorStore, patientStateStore, transitionStore)
    } else {
      console.error('No Rete container found')
}
  })
</script>

<template>
	<div ref="rete" class="rete"></div>
	<div class="sidebar">
		<h1>Patient 1007</h1>
	</div>
</template>

<style scoped>
.rete {
  position: relative;
  height: 90vh;
  width: 60%;
  font-size: 1rem;
  background: white;
  text-align: left;
  line-height: 1;
}

  .sidebar {
    position: absolute;
    top: 0;
    right: 0;
    width: 40%;
    height: 100%;
    background: #f0f0f0;
    padding: 20px;
    overflow: auto;
  }
</style>
