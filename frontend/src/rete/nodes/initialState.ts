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
  width = 180
  height = 100

  constructor() {
    super("InitialState")

    this.addOutput("next", new Classic.Output(socket, "next", false))
  }

  data() {
    return {}
  }
}