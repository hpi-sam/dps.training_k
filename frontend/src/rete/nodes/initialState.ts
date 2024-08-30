import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class InitialStateNode
  extends Classic.Node<
    {},
    { next: Classic.Socket }
  >
  implements DataflowNode
{
  width = 120
  height = 120

  constructor() {
    super("Start Zustand")

    this.addOutput("next", new Classic.Output(socket, undefined, false))
  }

  data() {
    return {}
  }
}