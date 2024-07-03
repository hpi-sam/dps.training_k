<script setup lang="ts">
  import { ref, Ref, onMounted } from 'vue'
  import { createEditor as createPatientEditor } from '@/rete/patient'
  import { usePatientEditorStore } from '@/stores/patienteditor/PatientEditor'
  import { usePatientStateStore } from '@/stores/patienteditor/PatientState'
  import { useTransitionStore } from '@/stores/patienteditor/Transition'
  import PatientInfoForm from '@/components/componentsPatientEditor/PatientInfoForm.vue'
  import PatientStateForm from '@/components/componentsPatientEditor/PatientStateForm.vue'

  interface ReteEditor {
    layout: () => Promise<void>;
    destroy: () => void;
  }

  const rete = ref(null)
  const reteEditor: Ref<ReteEditor | null> = ref(null)

  onMounted(async () => {
    const patientEditorStore = usePatientEditorStore()
    const patientStateStore = usePatientStateStore()
    const transitionStore = useTransitionStore()

    patientStateStore.clear()
    transitionStore.clear()

    patientStateStore.addPatientState(
      {
        id: 1,
        nodeId: '',
        nextTransition: 1,
        airway: "freie Atemwege",
        breathingRate: 1,
        oxygenSaturation: 1,
        breathing: "vertiefte Atmung",
        breathingSound: true,
        breathingLoudness: "sehr leises AG hörbar",
        heartRate: 1,
        pulsePalpable:"peripher tastbar",
        rivaRocci: "1/1",
        consciousness: "wach, orientiert",
        pupils: "mittelweit",
        psyche: "unauffällig",
        skinFining: "trocken",
        skinDiscoloration: "rosig",
        bgaOxy: 601,
        bgaSbh: 652,
        hb: 401,
        bz: 916,
        clotting: 100,
        liver: 111,
        kidney: 120,
        infarct: 134,
        lactate: 144,
        extremities: 523,
        thorax: 340,
        trauma: 108,
        ultraschall: 621,
        ekg: 746,
        zvd: 805 
      }
    )

    patientStateStore.addPatientState(
      {
        id: 2,
        nodeId: '',
        nextTransition: 2,
        airway: "freie Atemwege",
        breathingRate: 2,
        oxygenSaturation: 1,
        breathing: "vertiefte Atmung",
        breathingSound: true,
        breathingLoudness: "sehr leises AG hörbar",
        heartRate: 1,
        pulsePalpable:"peripher tastbar",
        rivaRocci: "1/1",
        consciousness: "wach, orientiert",
        pupils: "mittelweit",
        psyche: "unauffällig",
        skinFining: "trocken",
        skinDiscoloration: "rosig",
        bgaOxy: 601,
        bgaSbh: 652,
        hb: 401,
        bz: 916,
        clotting: 100,
        liver: 111,
        kidney: 120,
        infarct: 134,
        lactate: 144,
        extremities: 523,
        thorax: 340,
        trauma: 108,
        ultraschall: 621,
        ekg: 746,
        zvd: 805 
      }
    )

    patientStateStore.addPatientState(
      {
        id: 3,
        nodeId: '',
        nextTransition: 2,
        airway: "freie Atemwege",
        breathingRate: 3,
        oxygenSaturation: 1,
        breathing: "vertiefte Atmung",
        breathingSound: true,
        breathingLoudness: "sehr leises AG hörbar",
        heartRate: 1,
        pulsePalpable:"peripher tastbar",
        rivaRocci: "1/1",
        consciousness: "wach, orientiert",
        pupils: "mittelweit",
        psyche: "unauffällig",
        skinFining: "trocken",
        skinDiscoloration: "rosig",
        bgaOxy: 601,
        bgaSbh: 652,
        hb: 401,
        bz: 916,
        clotting: 100,
        liver: 111,
        kidney: 120,
        infarct: 134,
        lactate: 144,
        extremities: 523,
        thorax: 340,
        trauma: 108,
        ultraschall: 621,
        ekg: 746,
        zvd: 805 
      }
    )

    patientStateStore.addPatientState(
      {
        id: 4,
        nodeId: '',
        nextTransition: null,
        airway: "freie Atemwege",
        breathingRate: 4,
        oxygenSaturation: 1,
        breathing: "vertiefte Atmung",
        breathingSound: true,
        breathingLoudness: "sehr leises AG hörbar",
        heartRate: 1,
        pulsePalpable:"peripher tastbar",
        rivaRocci: "1/1",
        consciousness: "wach, orientiert",
        pupils: "mittelweit",
        psyche: "unauffällig",
        skinFining: "trocken",
        skinDiscoloration: "rosig",
        bgaOxy: 601,
        bgaSbh: 652,
        hb: 401,
        bz: 916,
        clotting: 100,
        liver: 111,
        kidney: 120,
        infarct: 134,
        lactate: 144,
        extremities: 523,
        thorax: 340,
        trauma: 108,
        ultraschall: 621,
        ekg: 746,
        zvd: 805 
      }
    )

    transitionStore.addTransition(
      {
        id: 1,
        nodeId: '',
        firstCondition: Number.NEGATIVE_INFINITY,
        nextStates: [2, 3]
      }
    )

    transitionStore.addTransition(
      {
        id: 2,
        nodeId: '',
        firstCondition: Number.NEGATIVE_INFINITY,
        nextStates: [4]
      }
    )

    if (rete.value) {
      reteEditor.value = await createPatientEditor(rete.value as HTMLElement, patientEditorStore, patientStateStore, transitionStore)
      await reteEditor?.value?.layout()
    } else {
      console.error('No Rete container found')
    }

  })
</script>

<template>
	<div ref="rete" class="rete" />
	<div v-if="false" class="sidebar">
		<PatientInfoForm />
	</div>
	<div class="sidebar">
		<PatientStateForm />
		<button @click="reteEditor?.layout(); console.log('Clicked Layout-Button')">
			Layout
		</button>
	</div>
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

  .sidebar {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 400px;
    background: #f0f0f0;
    padding: 20px;
    overflow: auto;
  }
</style>
