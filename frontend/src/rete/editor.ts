import { ref } from 'vue'
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
import { openPatientState } from '@/components/ModulePatientEditor.vue'
import { Modules } from "./modules.js"
import { clearEditor } from "./utils.js"
import { createNode, exportEditor, importEditor } from "./import.js"
import { createEngine } from "./processing.js"

import { Schemes, AreaExtra, Context, Connection } from './types'
import CustomDropdown from './customization/CustomDropdown.vue'
import { DropdownControl } from './dropdown'
import data from './data/data.json'
import { StateNode } from './nodes/index'

const editorMode = ref<string>("patient")

export async function createEditor(container: HTMLElement) {
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

    const contextMenu = new ContextMenuPlugin<Schemes>({
      items: ContextMenuPresets.classic.setup([
        ['State', () => createNode(context, "State", {})],
        ["Transition", () => createNode(context, "Transition", {})],
        ["Input", () => createNode(context, "Input", { key: "in" })],
        ["Output", () => createNode(context, "Output", { key: "out" })],
        ["Action", () => createNode(context, "Action", {})]
      ])
    })
  
    editor.use(area)
    area.use(vueRender)
    area.use(connection)
    area.use(contextMenu)

  area.area.setZoomHandler(null)

  area.addPipe(context => {
    if (context.type === 'nodepicked') {
      const node = editor.getNode(context.data.id)
      if (node instanceof StateNode) {
        openPatientState(node.id)
      }
      return
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
  
  const { dataflow, process } = createEngine(editor as any, area as any)
  editor.use(dataflow as any)

  // Modules

  let patientModuleData = data.flow
  let transitionModulesData = data.transitions
  let componentModulesData = data.components

  const patientModule = new Modules<Schemes>(
    () => true,
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
    (id) => transitionModulesData.find((module) => module.id === id) !== undefined,
    async (id, editor) => {
      const data = transitionModulesData.find((module) => module.id === id)?.flow

      if (!data) throw new Error("cannot find module "+id)
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
    (id) => componentModulesData.find((module) => module.id === id) !== undefined,
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
    dataflow,
    process,
    transitionModulesData,
    transitionModules,
    componentModulesData,
    componentModules
  }

  await process()

  function saveModule() {
    const data = exportEditor(context)

    if (editorMode.value === "patient") {
      patientModuleData = data as any
    } else if (editorMode.value === "transition") {
      const module = transitionModulesData.find(
        (module) => module.id === currentModuleId
      )
      if (module) module.flow = data as any
    } else if (editorMode.value === "component") {
      const module = componentModulesData.find(
        (module) => module.id === currentModuleId
      )
      if (module) module.flow = data as any
    }
  }

  let currentModuleId: null | string = null

  async function openModule(id: string, type: string) {
    if (editor.getNodes().length) saveModule()

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

  function getModules() {
    return {
      patientModuleData,
      transitionModulesData,
      componentModulesData
    }
  }

  return {
    getModules,
    saveModule,
    restoreModule: () => {
      openModule(currentModuleId!, editorMode.value)
    },
    newTransitionModule: (id: string) => {
      transitionModulesData = [ ...transitionModulesData, {id: id, flow: []}]
    },
    newComponentModule: (id: string) => {
      componentModulesData = [ ...componentModulesData, {id: id, flow: []}]
    },
    openModule,
    layout: async () => {
      await arrange.layout()
      AreaExtensions.zoomAt(area, editor.getNodes())
    },
    destroy: () => {
      console.log("area.destroy1", area.nodeViews.size)

      area.destroy()
    }
  }
}