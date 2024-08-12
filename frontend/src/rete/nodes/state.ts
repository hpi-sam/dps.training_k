import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class StateNode
  extends Classic.Node<
    { value: Classic.Socket }
  >
  implements DataflowNode {
  width = 180
  height = 140
  constructor() {
    super("State")

    this.addInput("value", new Classic.Input(socket))
    this.addOutput("value", new Classic.Output(socket))
  }
  data() {
    const value = this.controls["value"].value

    return {
      value
    }
  }

  serialize() {
    return {
      value: this.controls.value.value
    }
  }
}
