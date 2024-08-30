import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class StateNode
  extends Classic.Node<
    { in: Classic.Socket },
    { next: Classic.Socket }
  >
  implements DataflowNode
{
  width = 120
  height = 120

  constructor() {
    super("Zustand")

    this.addInput("in", new Classic.Input(socket, undefined, true))
    this.addOutput("next", new Classic.Output(socket, undefined, false))
  }

  data() {
    return {}
  }
}