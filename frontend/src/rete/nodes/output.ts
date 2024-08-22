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
  width = 180
  height = 140

  constructor(initial: string) {
    super("Output")

    this.addControl("key", new Classic.InputControl("text", { initial }))
    this.addInput("in", new Classic.Input(socket, "in"))
  }

  data() {
    return {}
  }

  serialize() {
    return {
      key: this.controls.key.value
    }
  }
}
