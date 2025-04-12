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
  width = 120
  height = 120

  constructor(initial: string, change?: (value: string) => void) {
    super("Start")

    this.addControl("key", new Classic.InputControl("text", { initial, change }))
    this.addOutput("out", new Classic.Output(socket, undefined, false))
  }

  data() {
    return {
      key: this.controls.key.value
    }
  }
}
