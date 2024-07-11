import { ClassicPreset as Classic } from "rete";
import { DataflowNode } from "rete-engine";
import { socket } from "../sockets";

export class NumberNode
  extends Classic.Node<
    { value: Classic.Socket },
    { value: Classic.Socket },
    { value: Classic.InputControl<"number"> }
  >
  implements DataflowNode {
  width = 180;
  height = 140;
  constructor(initial: number, change?: (value: number) => void) {
    super("Number");

    this.addOutput("value", new Classic.Output(socket, "Number"));
    this.addControl(
      "value",
      new Classic.InputControl("number", { initial, change })
    );
  }
  data() {
    const value = this.controls["value"].value;

    return {
      value
    };
  }

  serialize() {
    return {
      value: this.controls.value.value
    };
  }
}
