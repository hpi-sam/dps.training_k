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
  width = 180
  height = 120

  constructor() {
    super("State")

    this.addInput("in", new Classic.Input(socket, "in"))
    this.addOutput("next", new Classic.Output(socket, "next"))
  }

  data() {
    return {}
  }
}