import { ClassicPreset as Classic } from "rete"
import { socket } from "../sockets"

export class StateNode extends Classic.Node<{ value: Classic.Socket }> {
  width = 180
  height = 140
  constructor() {
    super("State")

    this.addInput("value", new Classic.Input(socket))
    this.addOutput("value", new Classic.Output(socket))
  }
}
