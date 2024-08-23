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

  constructor(initial: string, change?: (value: string) => void) {
    super("Input")

    this.addControl("key", new Classic.InputControl("text", { initial, change }))
    this.addOutput("out", new Classic.Output(socket, "out"))
  }

  data() {
    return {
      key: this.controls.key.value
    }
  }
}
