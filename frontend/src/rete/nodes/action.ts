import { ClassicPreset as Classic } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"
import { ActionIDs } from "../constants"

export interface DropdownOption {
  name: string;
  value: string;
}

export class DropdownControl extends Classic.Control {
  selection: DropdownOption
  optionsList: DropdownOption[]

  constructor(optionsList: DropdownOption[], initial?: DropdownOption, change?: (option: DropdownOption) => void) {
    super()
    this.optionsList = optionsList || []
    this.selection = initial || this.optionsList[0]
    this.onChange = change as any
  }

  setValue(option: DropdownOption): void {
    this.selection = option
    if (this.onChange) {
      this.onChange(option)
    }
  }

  onChange(option: DropdownOption): void {
    this.setValue(option)
  }
}

export class ActionNode
  extends Classic.Node<
    { input: Classic.Socket; true: Classic.Socket; false: Classic.Socket },
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

    this.addInput("input", new Classic.Input(socket, "input"))
    this.addOutput("true", new Classic.Output(socket, "true"))
    this.addOutput("false", new Classic.Output(socket, "false"))
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
      new Classic.InputControl("number", { initial: initialQuantity, change: changeQuantity })
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