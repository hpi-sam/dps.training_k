<script setup lang="ts">
  import { ref, onMounted, watch, computed } from 'vue'
  import { createEditor as createPatientEditor } from '@/rete/editor'
  import PatientInfoForm from '@/components/componentsPatientEditor/PatientInfoForm.vue'
  import PatientStateForm from '@/components/componentsPatientEditor/PatientStateForm.vue'
  import 'antd/dist/reset.css'
  import { Editor } from '@/rete/types'
  import data from '@/rete/data/data.json'

  const patientModule = ref("" as string)
  const transitionModules = ref([] as string[])
  const componentModules = ref([] as string[])
  const editorContainer = ref(null)
  const editor = ref(null as unknown as Editor)

  onMounted(async () => {
    editor.value = await createPatientEditor(editorContainer.value as unknown as HTMLElement)
    
    await editor.value?.layout()
    
    if (editor.value) {
      patientModule.value = editor.value.getModules().patientModuleData
      transitionModules.value = editor.value.getModules().transitionModulesData
      componentModules.value = editor.value.getModules().componentModulesData
      editor.value.openModule('', 'patient')
    }

    loadPatientInfo()
    loadPatientStates()
  })

  function loadPatientInfo() {
    info.value = data.info
  }

  function loadPatientStates() {
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

function saveModule() {
  editor.value?.saveModule()
}

function restoreModule() {
  editor.value?.restoreModule()
}

function exportData() {
  saveModule()
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
</script>

<script lang="ts">
  const patientInfoFormIsVisible = ref(true)

  export function openPatientState(stateId: string) {
    patientInfoFormIsVisible.value = false
    currentStateId.value = stateId
  }
  export const info = ref({} as any)
  export const states = ref([] as any)
  export const currentStateId = ref('')
  export const currentState = ref(computed(() => states.value.find((state) => state.id === currentStateId.value)))
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
		<p>Komponenten</p>
		<button
			v-for="module in componentModules as any"
			:key="module.id"
			@click="openModule(module.id, 'component')"
		>
			{{ module.id }}
		</button>
		<p>Bearbeitung</p>
		<button size="small" @click="newTransitionModule">
			Neue Transition
		</button>
		<button size="small" @click="newComponentModule">
			Neue Komponente
		</button>
		<button size="small" @click="saveModule">
			Save
		</button>
		<button size="small" @click="restoreModule">
			Restore
		</button>
		<button @click="editor?.layout(); console.log('Clicked Layout-Button')">
			Auto Layout
		</button>
		<button @click="exportData()">
			Export
		</button>
	</div>
	<div ref="editorContainer" class="rete" />
	<div v-show="patientInfoFormIsVisible" class="right-sidebar overlay">
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
    height: 100%;
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