import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class OutputNode
  extends Classic.Node<
    { in: Classic.Socket },
    {},
    { key: Classic.InputControl<"text"> }
  >
  implements DataflowNode {
  width = 120
  height = 120

  constructor(initial: string) {
    super("Option")

    this.addControl("key", new Classic.InputControl("text", { initial }))
    this.addInput("in", new Classic.Input(socket, undefined, true))
  }

  data() {
    return {
      key: this.controls.key.value
    }
  }

  serialize() {
    return {
      key: this.controls.key.value
    }
  }
}
