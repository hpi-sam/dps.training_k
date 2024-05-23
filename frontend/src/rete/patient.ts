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

type Node = StateNode | TransitionNode;
type Conn =
  | Connection<StateNode, TransitionNode>
  | Connection<TransitionNode, TransitionNode>
  | Connection<TransitionNode, StateNode>;
type Schemes = GetSchemes<Node, Conn>;

class Connection<A extends Node, B extends Node> extends Classic.Connection<
  A,
  B
> {}

class StateNode extends Classic.Node {
  width = 100
  height = 150

  constructor() {
    super('State')

    this.addInput('a', new Classic.Input(socket, ''))
    this.addOutput('value', new Classic.Output(socket, ''))
  }
}

class TransitionNode extends Classic.Node {
  width = 100
  height = 300

  constructor() {
    super('Transition')

    this.addInput('a', new Classic.Input(socket))
    this.addInput('b', new Classic.Input(socket))
    this.addInput('c', new Classic.Input(socket))
    this.addOutput('x', new Classic.Output(socket))
    this.addOutput('y', new Classic.Output(socket))
    this.addOutput('z', new Classic.Output(socket))
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

  connection.addPreset(ConnectionPresets.classic.setup())

  vueRender.addPreset(VuePresets.classic.setup())
  vueRender.addPreset(VuePresets.contextMenu.setup())
  vueRender.addPreset(VuePresets.minimap.setup())

  const a = new StateNode()
  const b = new StateNode()
  const t = new TransitionNode()

  await editor.addNode(a)
  await editor.addNode(b)
  await editor.addNode(t)

  await editor.addConnection(new Connection(a, 'value', t, 'a'))
  await editor.addConnection(new Connection(b, 'value', t, 'b'))

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
