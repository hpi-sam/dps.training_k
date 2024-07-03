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

<script lang="ts">
  const patientInfoFormIsVisible = ref(true)

  export function showPatientStateForm() {
    patientInfoFormIsVisible.value = false
  }
</script>

<template>
	<div class="left-sidebar">
		<button @click="patientInfoFormIsVisible = true">
			Patienteninfos bearbeiten
		</button>
		<button @click="reteEditor?.layout(); console.log('Clicked Layout-Button')">
			Auto Layout
		</button>
	</div>
	<div ref="rete" class="rete" />
	<div v-if="patientInfoFormIsVisible" class="right-sidebar overlay">
		<PatientInfoForm />
	</div>
	<div class="right-sidebar">
		<PatientStateForm />
	</div>
</template>

<style scoped>
  .left-sidebar {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    background: transparent;
    padding: 20px;
    overflow: auto;
    z-index: 1;
  }

  .left-sidebar button {
    margin-bottom: 10px;
    width: fit-content;
    padding: 10px;

    height: 40px;
    border: none;
    border-radius: .5rem;
    font-size: 1.25rem;
    line-height: 1.25rem;
    background-color: var(--green);
    color: white;
  }

  .rete {
    position: relative;
    height: 90vh;
    width: calc(100% - 400px);
    font-size: 1rem;
    background: white;
    text-align: left;
    line-height: 1;
  }

  .right-sidebar {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 400px;
    background: #f0f0f0;
    padding: 20px;
    overflow: auto;
  }

  .overlay {
    z-index: 1;
  }
</style>
