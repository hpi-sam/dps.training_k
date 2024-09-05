import { ref, watch } from 'vue'
import { ClassicPreset as Classic, NodeEditor } from 'rete'
import { AreaExtensions, AreaPlugin } from 'rete-area-plugin'
import { ConnectionPlugin } from 'rete-connection-plugin'
import { VuePlugin, Presets as VuePresets } from 'rete-vue-plugin'
import {
  AutoArrangePlugin,
  Presets as ArrangePresets,
} from 'rete-auto-arrange-plugin'
import { CustomContextMenu, Presets as ContextMenuPresets } from './customization/CustomContextMenu'
import { ClassicFlow, getSourceTarget } from 'rete-connection-plugin'
import { openPatientState } from '@/components/screensTrainer/ScreenPatientEditor.vue'
import { Modules } from "./modules.js"
import { clearEditor } from "./utils.js"
import { createNode, exportEditor, importEditor } from "./import.js"
import { Schemes, AreaExtra, Context, Connection } from './types'
import CustomDropdown from './customization/CustomDropdown.vue'
import { DropdownControl } from './dropdown'
import { StateNode, InitialStateNode, InputNode, OutputNode } from './nodes/index'
import CircleNode from './customization/CircleNode.vue'

export const editorMode = ref<string>("patient")

export async function createEditor(container: HTMLElement, data: any) {
  const editor = new NodeEditor<Schemes>()
  const area = new AreaPlugin<Schemes, AreaExtra>(container)
  const connection = new ConnectionPlugin<Schemes, AreaExtra>()
  const vueRender = new VuePlugin<Schemes, AreaExtra>()
  const arrange = new AutoArrangePlugin<Schemes, AreaExtra>()
  
  vueRender.addPreset(
    VuePresets.classic.setup({
      customize: {
        node(context) {
          if (context.payload instanceof StateNode 
            || context.payload instanceof InitialStateNode
            || context.payload instanceof InputNode
            || context.payload instanceof OutputNode
          ) {
            return CircleNode
            }
          return VuePresets.classic.Node
        },
      },
    })
  )

  const contextMenu = new CustomContextMenu<Schemes>({
    items: ContextMenuPresets.classic.setup([
      ['Start Zustand', () => createNode(context, "InitialState", {})],
      ['Zustand', () => createNode(context, "State", {})],
      ["Übergang", () => createNode(context, "Transition", {})]
    ])
  })

  watch(editorMode, (newMode) => {
    if (newMode === "patient") {
      contextMenu.updateItems(ContextMenuPresets.classic.setup([
        ['Start Zustand', () => createNode(context, "InitialState", {})],
        ['Zustand', () => createNode(context, "State", {})],
        ["Übergang", () => createNode(context, "Transition", {})]
      ]))
    } else if (newMode === "transition") {
      contextMenu.updateItems(ContextMenuPresets.classic.setup([
        ["Start", () => createNode(context, "Input", { key: "in" })],
        ["Option", () => createNode(context, "Output", { key: "out" })],
        ["Aktion", () => createNode(context, "Action", {})],
        ["Material", () => createNode(context, "Material", {})],
        ["Komponente", () => createNode(context, "Component", {})]
      ]))
    } else if (newMode === "component") {
      contextMenu.updateItems(ContextMenuPresets.classic.setup([
        ["Start", () => createNode(context, "Input", { key: "in" })],
        ["Option", () => createNode(context, "Output", { key: "out" })],
        ["Aktion", () => createNode(context, "Action", {})],
        ["Material", () => createNode(context, "Material", {})]
      ]))
    }
  })

  editor.use(area)
  area.use(vueRender)
  area.use(connection)
  area.use(contextMenu)

  area.area.setZoomHandler(null)

  area.addPipe(context => {
    if (context.type === 'nodepicked') {
      const node = editor.getNode(context.data.id)
      if (node instanceof StateNode || node instanceof InitialStateNode) {
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
    transitionModulesData,
    transitionModules,
    componentModulesData,
    componentModules
  }

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
      context.transitionModulesData = transitionModulesData
    },
    newComponentModule: (id: string) => {
      componentModulesData = [ ...componentModulesData, {id: id, flow: []}]
      context.componentModulesData = componentModulesData
    },
    openModule,
    deleteModule: () => {
      if (editorMode.value === 'transition') {
        transitionModulesData = transitionModulesData.filter((module) => module.id !== currentModuleId)
        context.transitionModulesData = transitionModulesData
      } else if (editorMode.value === "component") {
        componentModulesData = componentModulesData.filter((module) => module.id !== currentModuleId)
        context.componentModulesData = componentModulesData
      }
    },
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