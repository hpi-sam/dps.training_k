import { ref, watch } from 'vue'
import { ClassicPreset as Classic, NodeEditor } from 'rete'
import { AreaExtensions, AreaPlugin } from 'rete-area-plugin'
import { ConnectionPlugin } from 'rete-connection-plugin'
import { VuePlugin, Presets as VuePresets } from 'rete-vue-plugin'
import {
  AutoArrangePlugin,
  Presets as ArrangePresets,
} from 'rete-auto-arrange-plugin'
import { ContextMenuPlugin, Presets as ContextMenuPresets } from 'rete-context-menu-plugin'
import { ClassicFlow, getSourceTarget } from 'rete-connection-plugin'

import { loadPatientState } from '@/components/componentsPatientEditor/PatientStateForm.vue'
import { showPatientStateForm } from '@/components/ModulePatientEditor.vue'
import { Modules } from "./modules.js"
import { clearEditor } from "./utils.js"
import { createNode, exportEditor, importEditor } from "./import.js"
import { createEngine } from "./processing.js"

import { Schemes, AreaExtra, Context, Connection } from './types'
import CustomDropdown from './customization/CustomDropdown.vue'
import { DropdownControl } from './dropdown'
import data from './data/data.json'

const editorMode = ref<string>("patient")

export async function createEditor(
  container: HTMLElement,
  patientEditorStore: any,
  patientStateStore: any,
  transitionStore: any
) {
  const editor = new NodeEditor<Schemes>()
  const area = new AreaPlugin<Schemes, AreaExtra>(container)
  const connection = new ConnectionPlugin<Schemes, AreaExtra>()
  const vueRender = new VuePlugin<Schemes, AreaExtra>()
  const arrange = new AutoArrangePlugin<Schemes, AreaExtra>()
  
  /*vueRender.addPreset(
    VuePresets.classic.setup({
      customize: {
        node(context) {
          if (context.payload.label === 'State') {
            return CircleNode
            } else if (context.payload.label === 'Transition') {
            return SquareNode
            }
            return VuePresets.classic.Node
            },
      },
    })
  )*/

    let contextMenu = new ContextMenuPlugin<Schemes>({
      items: ContextMenuPresets.classic.setup([])
    })
  
    function updateContextMenu() {
      let items = <BSchemes>[]
  
      if (editorMode.value === "patient") {
        items = ContextMenuPresets.classic.setup([
          ['State', () => createNode(context, "State", { value: 0 })],
          ["Module", () => createNode(context, "Module", { name: "" })]
        ])
      } else if (editorMode.value === "transition") {
        items = ContextMenuPresets.classic.setup([
          ["Input", () => createNode(context, "Input", { key: "key" })],
          ["Output", () => createNode(context, "Output", { key: "key" })],
          ["Module", () => createNode(context, "Module", { name: "" })],
          ["Action", () => createNode(context, "Action", {})]
        ])
      } else if (editorMode.value === "component") {
        items = ContextMenuPresets.classic.setup([
          ["Input", () => createNode(context, "Input", { key: "key" })],
          ["Output", () => createNode(context, "Output", { key: "key" })],
          ["Module", () => createNode(context, "Module", { name: "" })],
          ["Action", () => createNode(context, "Action", {})]
        ])
      }
  
      contextMenu = new ContextMenuPlugin<Schemes>({ items })
    }
  
    updateContextMenu()
    watch(editorMode, updateContextMenu)
  
    editor.use(area)
    area.use(vueRender)
    area.use(connection)
    area.use(contextMenu)
  

  area.area.setZoomHandler(null)

  area.addPipe(context => {
    if (context.type === 'nodepicked') {
      const node = editor.getNode(context.data.id)
      showPatientStateForm()
      loadPatientState(node.id)
    }
    return context
  })
  
  connection.addPreset(() => new ClassicFlow({
    makeConnection(from, to, context) {
      const [source, target] = getSourceTarget(from, to) || [null, null]
      const { editor } = context

      // no connections with nodes with the same label
      // if (editor.getNode(source?.nodeId || '').label ===  editor.getNode(target?.nodeId || '').label) return false
  
      if (source && target) {
        editor.addConnection(
          new Connection(
            editor.getNode(source.nodeId),
            source.key as never,
            editor.getNode(target.nodeId),
            target.key as never
          )
        )
        return true
      }
    }
  }))

  vueRender.addPreset(VuePresets.classic.setup())
  vueRender.addPreset(VuePresets.contextMenu.setup())

  vueRender.addPreset(
    VuePresets.classic.setup({
      customize: {
        control(data) {
          if (data.payload instanceof DropdownControl) {
            return CustomDropdown
          }
          if (data.payload instanceof Classic.InputControl) {
            return VuePresets.classic.Control
          }
        }
      }
    })
  )
  
  arrange.addPreset(ArrangePresets.classic.setup())
  area.use(arrange)
  AreaExtensions.zoomAt(area, editor.getNodes())
  AreaExtensions.simpleNodesOrder(area)
  const selector = AreaExtensions.selector()
  const accumulating = AreaExtensions.accumulateOnCtrl()
  AreaExtensions.selectableNodes(area, selector, { accumulating })
  
  const { dataflow, process } = createEngine(editor, area)
  editor.use(dataflow)

  // Modules

  const patientModuleData = data.flow
  const transitionModulesData = data.transitions
  const componentModulesData = data.components

  const patientModule = new Modules<Schemes>(
    true,
    async (id, editor) => {
      const data = patientModuleData

      if (!data) throw new Error("cannot find module")
      await importEditor(
        {
          ...context,
          editor
        },
        data
      )
    }
  )

  const transitionModules = new Modules<Schemes>(
    (id) => transitionModulesData.find((module) => module.id === id),
    async (id, editor) => {
      const data = transitionModulesData.find((module) => module.id === id)?.flow

      if (!data) throw new Error("cannot find module")
      await importEditor(
        {
          ...context,
          editor
        },
        data
      )
    }
  )

  const componentModules = new Modules<Schemes>(
    (id) => componentModulesData.find((module) => module.id === id),
    async (id, editor) => {
      const data = componentModulesData.find((module) => module.id === id)?.flow

      if (!data) throw new Error("cannot find module")
      await importEditor(
        {
          ...context,
          editor
        },
        data
      )
    }
  )

  const context: Context = {
    editor,
    area,
    modules: transitionModules,
    dataflow,
    process
  }

  await process()

  let currentModuleId: null | string = null

  async function openModule(id: string, type: string) {
    currentModuleId = null

    await clearEditor(editor)

    editorMode.value = type

    let module = null

    if (type === "patient") {
      module = patientModule.findModule(id)
    } else if (type === "transition") {
      module = transitionModules.findModule(id)
    } else if (type === "component") {
      module = componentModules.findModule(id)
    }

    if (module) {
      currentModuleId = id
      await module.apply(editor)
    }

    await arrange.layout()
    AreaExtensions.zoomAt(area, editor.getNodes())
  }
  (window as any).area = area

  await arrange.layout()

  return {
    getModules() {
      return {
        patientModuleData,
        transitionModulesData,
        componentModulesData
      }
    },
    saveModule: () => {
      if (currentModuleId) {
        const data = exportEditor(context)
        transitionModulesData[currentModuleId] = data

        const json = JSON.stringify(data)
        const blob = new Blob([json], { type: 'text/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${currentModuleId}.json`
        a.click()
        URL.revokeObjectURL(url)
      }
    },
    restoreModule: () => {
      if (currentModulePath) openModule(currentModulePath)
    },
    newModule: (id: string) => {
      transitionModulesData[id] = { nodes: [], connections: [] }
    },
    openModule,
    layout: async () => {
      await arrange.layout()
      console.log("Layout arranged")
      AreaExtensions.zoomAt(area, editor.getNodes())
    },
    destroy: () => {
      console.log("area.destroy1", area.nodeViews.size)

      area.destroy()
    }
  }
}