import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class InputNode
  extends Classic.Node<
    {},
    { out: Classic.Socket },
    { key: Classic.InputControl<"text"> }
  >
  implements DataflowNode {
  width = 180
  height = 140
  value: any = null

  constructor(initial: string) {
    super("Input")

    this.addControl("key", new Classic.InputControl("text", { initial }))
    this.addOutput("out", new Classic.Output(socket, "out"))
  }

  data() {
    return {
      value: this.value
    }
  }

  serialize() {
    return {
      key: this.controls.key.value
    }
  }
}
