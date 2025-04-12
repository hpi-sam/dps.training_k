import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"
import { MaterialIDs } from "../constants"
import { DropdownControl, DropdownOption } from "../dropdown"

export class MaterialNode
  extends Classic.Node<
    { in: Classic.Socket },
    { true: Classic.Socket; false: Classic.Socket },
    { selection: DropdownControl, quantity: Classic.InputControl<"number"> }
  >
  implements DataflowNode
{
  width = 180
  height = 230

  constructor(
    initialSelection?: DropdownOption,
    changeSelection?: (option: DropdownOption) => void,
    initialQuantity?: number,
    changeQuantity?: (value: number) => void
  ) {
    super("Material")

    MaterialIDs.sort((a, b) => a.name.localeCompare(b.name))

    this.addInput("in", new Classic.Input(socket, "in", true))
    this.addOutput("true", new Classic.Output(socket, "ja", false))
    this.addOutput("false", new Classic.Output(socket, "nein", false))
    this.addControl(
      "selection",
      new DropdownControl(
        MaterialIDs.map((material) => ({
          name: material.name,
          value: material.id,
        })),
        initialSelection,
        changeSelection,
      )
    )
    this.addControl(
      "quantity",
      new Classic.InputControl("number", { initial: initialQuantity || 1, change: changeQuantity })
    )
  }

  selection() {
    return this.controls["selection"].selection
  }

  quantity() {
    return this.controls["quantity"].value
  }

  data() {
    const value = this.controls["selection"].selection

    return {
      value,
    }
  }
}