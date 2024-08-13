import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class isInRangeNode
  extends Classic.Node<
  { input: Classic.Socket, inside: Classic.Socket, outside: Classic.Socket },
  { inside: Classic.Socket, outside: Classic.Socket },
  { fromValue: Classic.InputControl<"number">, toValue: Classic.InputControl<"number"> }
  >
  implements DataflowNode {
  width = 180
  height = 230
  constructor(fromValue: number, toValue: number) {
    super("ist im Wertebereich")

    this.addInput("input", new Classic.Input(socket, "input"))
    this.addOutput("inside", new Classic.Output(socket, "innerhalb"))
    this.addOutput("outside", new Classic.Output(socket, "außerhalb"))
    this.addControl(
        "fromValue",
        new Classic.InputControl("number", { initial: fromValue })
    )
    this.addControl(
        "toValue",
        new Classic.InputControl("number", { initial: toValue })
    )
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
