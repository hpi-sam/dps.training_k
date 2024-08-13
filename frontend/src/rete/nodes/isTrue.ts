import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"

export class DropdownControl extends Classic.Control {
    constructor(public list: string[]) {
      super()
    }
  }

export class isTrueNode
  extends Classic.Node<
  { input: Classic.Socket, true: Classic.Socket, false: Classic.Socket },
  { true: Classic.Socket, false: Classic.Socket },
  { value: DropdownControl }
  >
  implements DataflowNode {
  width = 180
  height = 190
  constructor() {
    super("ist wahr")

    this.addInput("input", new Classic.Input(socket, "input"))
    this.addOutput("true", new Classic.Output(socket, "wahr"))
    this.addOutput("false", new Classic.Output(socket, "falsch"))
    this.addControl(
      "value",
      new DropdownControl(["A", "B", "C"])
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
