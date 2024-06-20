import { ClassicPreset as Classic, GetSchemes, NodeEditor } from 'rete'
import { Area2D, AreaExtensions, AreaPlugin } from 'rete-area-plugin'
import {
  ConnectionPlugin,
  Presets as ConnectionPresets,
} from 'rete-connection-plugin'
import { VuePlugin, VueArea2D, Presets as VuePresets } from 'rete-vue-plugin'
import {
  AutoArrangePlugin,
  Presets as ArrangePresets,
} from 'rete-auto-arrange-plugin'
import { Zoom } from 'rete-area-plugin'
import {
  ContextMenuPlugin,
  ContextMenuExtra,
  Presets as ContextMenuPresets,
} from 'rete-context-menu-plugin'
import { ClassicFlow, getSourceTarget } from 'rete-connection-plugin'
import CircleNode from './customization/CircleNode.vue'
import SquareNode from './customization/SquareNode.vue'

type Node = StateNode | TransitionNode;
type Conn =
  | Connection<StateNode, TransitionNode>
  | Connection<TransitionNode, StateNode>;
type Schemes = GetSchemes<Node, Conn>;

class Connection<A extends Node, B extends Node> extends Classic.Connection<A,B> {}

class StateNode extends Classic.Node {
  width = 100
  height = 100

  constructor() {
    super('State')

    this.label = 'State'

    this.addInput('in', new Classic.Input(socket, undefined, false))
    this.addOutput('out', new Classic.Output(socket, undefined, false))
  }
}

class TransitionNode extends Classic.Node {
  width = 150
  height = 100

  constructor() {
    super('Transition')

    this.label = 'Transition'

    this.addInput('in', new Classic.Input(socket, undefined, true))
    this.addOutput('out', new Classic.Output(socket, undefined, true))
  }
}

type AreaExtra =
  | Area2D<Schemes>
  | VueArea2D<Schemes>
  | ContextMenuExtra
  | MinimapExtra;

const socket = new Classic.Socket('socket')

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
  
  vueRender.addPreset(
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
  )
  
  const contextMenu = new ContextMenuPlugin<Schemes>({
    items: ContextMenuPresets.classic.setup([
      ['State', () => new StateNode()],
      ['Transition', () => new TransitionNode()],
    ]),
  })
  
  editor.use(area)
  area.use(vueRender)
  area.use(connection)
  area.use(contextMenu)

  area.area.setZoomHandler(null)
  
  connection.addPreset(() => new ClassicFlow({
    makeConnection(from, to, context) {
      const [source, target] = getSourceTarget(from, to) || [null, null]
      const { editor } = context

      // no connections with nodes with the same label
      if (editor.getNode(source?.nodeId || '').label ===  editor.getNode(target?.nodeId || '').label) return false
  
      if (source && target) {
        editor.addConnection(
          new Connection(
            editor.getNode(source.nodeId),
            source.key,
            editor.getNode(target.nodeId),
            target.key
          )
        )
        return true
      }
    }
  }))

  vueRender.addPreset(VuePresets.classic.setup())
  vueRender.addPreset(VuePresets.contextMenu.setup())

  // Create nodes from patient states and store them in an object
  for (const patientState of Object.values(patientStateStore.patientStates)) {
    const node = new StateNode()
    await editor.addNode(node)
    patientState.nodeId = node.id
  }

  // Create nodes from transitions and store them in an object
  for (const transition of Object.values(transitionStore.transitions)) {
    const node = new TransitionNode()
    await editor.addNode(node)
    transition.nodeId = node.id
  }

  
  // Create connections
  for (const patientState of Object.values(patientStateStore.patientStates)) {
    const node = editor.getNode(patientState.nodeId)
    const nextTransition = transitionStore.transitions[patientState.nextTransition]
    if (!nextTransition) continue
    const nextNode = editor.getNode(nextTransition.nodeId)
    await editor.addConnection(new Connection(node, 'out', nextNode, 'in'))
  }

  // Create connections
  for (const transition of Object.values(transitionStore.transitions)) {
    const node = editor.getNode(transition.nodeId)
    const nextState = patientStateStore.patientStates[transition.nextStates[0]]
    const nextNode = editor.getNode(nextState.nodeId)
    console.log("Transition: "+ node.id+" to "+nextNode)
    await editor.addConnection(new Connection(node, 'out', nextNode, 'in'))
  }
  
  const arrange = new AutoArrangePlugin<Schemes>()
  arrange.addPreset(ArrangePresets.classic.setup())
  area.use(arrange)
  await arrange.layout()

  AreaExtensions.zoomAt(area, editor.getNodes())

  AreaExtensions.simpleNodesOrder(area)

  const selector = AreaExtensions.selector()
  const accumulating = AreaExtensions.accumulateOnCtrl()

  AreaExtensions.selectableNodes(area, selector, { accumulating })

  return {
    layout: async () => {
      await arrange.layout()
      AreaExtensions.zoomAt(area, editor.getNodes())
    },
    destroy: () => area.destroy(),
  }
}