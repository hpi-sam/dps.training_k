import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"
import { ActionIDs } from "../constants"
import { DropdownControl, DropdownOption } from "../dropdown"

export class ActionNode
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
    super("Action")

    ActionIDs.sort((a, b) => a.name.localeCompare(b.name))

    this.addInput("in", new Classic.Input(socket, "in", true))
    this.addOutput("true", new Classic.Output(socket, "true", false))
    this.addOutput("false", new Classic.Output(socket, "false", false))
    this.addControl(
      "selection",
      new DropdownControl(
        ActionIDs.map((action) => ({
          name: action.name,
          value: action.id,
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