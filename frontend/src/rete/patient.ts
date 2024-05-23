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

import {
  ContextMenuPlugin,
  ContextMenuExtra,
  Presets as ContextMenuPresets,
} from 'rete-context-menu-plugin'
import { MinimapExtra, MinimapPlugin } from 'rete-minimap-plugin'

import { ClassicFlow, getSourceTarget } from 'rete-connection-plugin'

import CircleNode from './customization/CircleNode.vue'
import SquareNode from './customization/SquareNode.vue'

type Node = StateNode | TransitionNode;
type Conn =
  | Connection<StateNode, TransitionNode>
  | Connection<TransitionNode, StateNode>;
type Schemes = GetSchemes<Node, Conn>;

class Connection<A extends Node, B extends Node> extends Classic.Connection<
  A,
  B
> {}

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

export async function createEditor(container: HTMLElement) {
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
  const minimap = new MinimapPlugin<Schemes>()

  editor.use(area)

  area.use(vueRender)

  area.use(connection)
  area.use(contextMenu)
  area.use(minimap)

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
  vueRender.addPreset(VuePresets.minimap.setup())

  const a = new StateNode()
  const b = new StateNode()
  const t = new TransitionNode()

  await editor.addNode(a)
  await editor.addNode(b)
  await editor.addNode(t)

  await editor.addConnection(new Connection(a, 'out', t, 'in'))
  await editor.addConnection(new Connection(b, 'out', t, 'in'))

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
    destroy: () => area.destroy(),
  }
}
