<script setup lang="ts">
import PatientInfoForm from '@/components/componentsPatientEditor/PatientInfoForm.vue'
import PatientStateForm from '@/components/componentsPatientEditor/PatientStateForm.vue'
import { onMounted, watch } from 'vue'
import { createEditor as createPatientEditor, editorMode } from '@/rete/editor'
import 'antd/dist/reset.css'
import { Editor } from '@/rete/types'
import defaultData from '@/rete/data/data.json'
import { Screens, ScreenPosition, setScreen } from '@/components/ModuleTrainer.vue'

const patientModule = ref("" as any)
const transitionModules = ref([] as any)
const componentModules = ref([] as any)
const editorContainer = ref(null)
const editor = ref(null as unknown as Editor)
const data = ref(defaultData)

onMounted(async () => {
  await startEditor(data.value)
})

async function startEditor(data: any) {
  editor.value = await createPatientEditor(editorContainer.value as unknown as HTMLElement, data) as any as Editor
  
  await editor.value?.layout()

  if (editor.value) {
    patientModule.value = editor.value.getModules().patientModuleData
    transitionModules.value = editor.value.getModules().transitionModulesData
    componentModules.value = editor.value.getModules().componentModulesData
    editor.value.openModule('', 'patient')
  }
  
  loadPatientInfo(data)
  loadPatientStates(data)

  setTimeout(() => {
    editor.value?.layout()
  }, 100)
}

function loadPatientInfo(data: any) {
  info.value = data.info
}

function loadPatientStates(data: any) {
  states.value = data.states
}

function openPatient() {
  editor.value?.openModule('', 'patient').then(() => {
    editor.value?.layout()
  })
  patientInfoFormIsVisible.value = true
}

watch(editor, (newEditor) => {
  if (newEditor) {
    patientModule.value = newEditor.getModules().patientModuleData
    transitionModules.value = newEditor.getModules().transitionModulesData
    componentModules.value = newEditor.getModules().componentModulesData
    newEditor.openModule('', 'patient')
  }
})

function openModule(id: string, type: string) {
  editor.value?.openModule(id, type).then(() => {
    if (type != 'patient') {
      patientInfoFormIsVisible.value = false
      patientStateFormIsVisible.value = false
    }
    editor.value?.layout()
  })
}

function newTransitionModule() {
  const id = prompt('Transition Id')
  if (id) {
    editor.value?.newTransitionModule(id)
    transitionModules.value = editor.value.getModules().transitionModulesData
    openModule(id, 'transition')
  }
}

function newComponentModule() {
  const id = prompt('Komponenten Id')
  if (id) {
    editor.value?.newComponentModule(id)
    componentModules.value = editor.value.getModules().componentModulesData
    openModule(id, 'component')
  }
}

function deleteModule() {
  editor.value.deleteModule()
  transitionModules.value = editor.value.getModules().transitionModulesData
  componentModules.value = editor.value.getModules().componentModulesData
  openModule('', 'patient')
}

function exportData() {
  editor.value.saveModule()
  const data = {
    info: info.value,
    flow: editor.value?.getModules().patientModuleData,
    states: states.value,
    transitions: editor.value?.getModules().transitionModulesData,
    components: editor.value?.getModules().componentModulesData
  }
  const json = JSON.stringify(data)
  const blob = new Blob([json], { type: 'text/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'patient.json'
  a.click()
  URL.revokeObjectURL(url)
}

const reteWidth = computed(() => {
  return patientInfoFormIsVisible.value || patientStateFormIsVisible.value ? 'calc(100% - 400px)' : '100%'
})

function backToTrainer() {
  setScreen(Screens.EXERCISE_CREATION, ScreenPosition.LEFT)
  setScreen(Screens.RESOURCE_CREATION, ScreenPosition.RIGHT)    
}

defineExpose({
  data,
  startEditor,
})
</script>
<script lang="ts">
import { getCurrentInstance, ref, computed } from 'vue'
import { State } from '@/rete/types'

const instance = getCurrentInstance()
let proxy: any = null

if (instance) {
  proxy = instance.proxy
}

const patientInfoFormIsVisible = ref(true)
const patientStateFormIsVisible = ref(false)

export function changePatientData(newData: any) {
  if (proxy) {
    console.log('changePatientData', newData)
    // Delete the existing editor
    proxy.editor.value = null
    // Create a new editor with the new data
    proxy.startEditor(newData)
    // Update the data reference
    proxy.data.value = newData
  }
}

export function openPatientState(stateId: string) {
  patientInfoFormIsVisible.value = false
  patientStateFormIsVisible.value = true
  currentStateId.value = stateId
}

export const info = ref({} as any)
export const states = ref([] as State[])
export const currentStateId = ref('')
export const currentState = ref(computed(() => states.value.find((state) => state.id === currentStateId.value)))

export function addState(stateId: string) {
  const state: State = {
    id: stateId,
    airway: "freie Atemwege",
    breathingRate: 1,
    oxygenSaturation: 1,
    breathing: "vertiefte Atmung",
    breathingSound: true,
    breathingLoudness: "sehr leises AG hörbar",
    heartRate: 1,
    pulsePalpable: "peripher tastbar",
    rivaRocci: "1/1",
    consciousness: "wach, orientiert",
    pupils: "mittelweit",
    psyche: "unauffällig",
    skinFinding: "trocken",
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
  states.value.push(state)
}
</script>

<template>
	<div class="left-sidebar">
		<button @click="openPatient">
			Patient
		</button>
		<p>Transitionen</p>
		<button
			v-for="module in transitionModules as any"
			:key="module.id"
			@click="openModule(module.id, 'transition')"
		>
			{{ module.id }}
		</button>
		<button size="small" @click="newTransitionModule">
			Neue Transition
		</button>
		<p>Komponenten</p>
		<button
			v-for="module in componentModules as any"
			:key="module.id"
			@click="openModule(module.id, 'component')"
		>
			{{ module.id }}
		</button>
		<button size="small" @click="newComponentModule">
			Neue Komponente
		</button>
		<p>Bearbeitung</p>
		<button v-if="editorMode == 'transition'" @click="deleteModule()">
			Diese Transition löschen
		</button>
		<button v-if="editorMode == 'component'" @click="deleteModule()">
			Diese Komponente löschen
		</button>
		<button @click="editor?.layout()">
			Auto Layout
		</button>
		<button @click="exportData()">
			Export
		</button>
		<button @click="backToTrainer()">
			Zurück zum Trainer
		</button>
	</div>
	<div ref="editorContainer" class="rete" :style="{ width: reteWidth }" />
	<div v-show="patientInfoFormIsVisible" class="right-sidebar overlay">
		<PatientInfoForm />
	</div>
	<div v-show="patientStateFormIsVisible" class="right-sidebar">
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
    height: 100%;
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