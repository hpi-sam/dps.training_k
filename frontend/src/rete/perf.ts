import { ClassicPreset as Classic, GetSchemes, NodeEditor } from 'rete'
import { AreaExtensions, AreaPlugin } from 'rete-area-plugin'

import { VuePlugin, VueArea2D, Presets as VuePresets } from 'rete-vue-plugin'

class Node extends Classic.Node {
  constructor() {
    super('Perf')

    this.addInput('port', new Classic.Input(socket, 'Input'))
    this.addOutput('port', new Classic.Output(socket, 'Output'))
  }
}

class Connection<A extends Node, B extends Node> extends Classic.Connection<
  A,
  B
> {}

type Schemes = GetSchemes<Node, Connection<Node, Node>>;

type AreaExtra = VueArea2D<Schemes>;

const socket = new Classic.Socket('socket')

export async function createEditor(container: HTMLElement) {
  const editor = new NodeEditor<Schemes>()
  const area = new AreaPlugin<Schemes, AreaExtra>(container)

  const vueRender = new VuePlugin<Schemes, AreaExtra>()

  editor.use(area)

  area.use(vueRender)

  vueRender.addPreset(VuePresets.classic.setup())

  // eslint-disable-next-line no-restricted-globals
  const query = new URLSearchParams(location.search)
  const rows = Number(query.get('rows') || 0) || 12
  const cols = Number(query.get('cols') || 0) || 12

  let prev: null | Node = null
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const a = new Node()

      await editor.addNode(a)
      await area.translate(a.id, { x: col * 310, y: row * 190 })

      if (prev) {
        await editor.addConnection(new Connection(prev, 'port', a, 'port'))
      }
      prev = a
    }
  }

  AreaExtensions.zoomAt(area, editor.getNodes())

  AreaExtensions.simpleNodesOrder(area)

  AreaExtensions.selectableNodes(area, AreaExtensions.selector(), {
    accumulating: AreaExtensions.accumulateOnCtrl(),
  })

  return {
    destroy: () => area.destroy(),
  }
}
