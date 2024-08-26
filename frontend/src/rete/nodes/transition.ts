import { ClassicPreset as Classic, NodeEditor } from "rete"
import { DataflowNode } from "rete-engine"
import { socket } from "../sockets"
import { Module, Modules } from "../modules"
import { Schemes } from "../types"
import { DropdownControl, DropdownOption } from "../dropdown"

export class TransitionNode
  extends Classic.Node<
    Record<string, Classic.Socket>,
    Record<string, Classic.Socket>,
    { selection: DropdownControl }
  >
  implements DataflowNode {
  width = 180
  height = 140
  module: null | Module<Schemes> = null

  constructor(
    transitionModulesData: string[],
    private findModule: (id: string) => null | Module<Schemes>,
    private reset: (nodeId: string) => Promise<void>,
    updateUI: (nodeId: string) => void,
    initialSelection?: DropdownOption,
  ) {
    super("Transition")

    this.addControl(
      "selection",
      new DropdownControl(
        transitionModulesData.map((module) => ({name: module.id, value: module.id })),
        initialSelection,
        async () => {
          await this.update()
          await updateUI(this.id)
        }
      )
    )
    this.update()
  }

  async update() {
    this.module = this.findModule(this.controls.selection.selection.name)

    await this.reset(this.id)
    if (this.module) {
      const editor = new NodeEditor<Schemes>()
      await this.module.apply(editor)
      
      const { inputs, outputs } = Modules.getPorts(editor)
      this.syncPorts(inputs, outputs)
    } else this.syncPorts([], [])
  }
  
  syncPorts(inputs: string[], outputs: string[]) {
    Object.keys(this.inputs).forEach((key: keyof typeof this.inputs) =>
      this.removeInput(key)
    )
    Object.keys(this.outputs).forEach((key: keyof typeof this.outputs) =>
      this.removeOutput(key)
    )

    inputs.forEach((key) => {
      this.addInput(key, new Classic.Input(socket, key, true))
    })
    outputs.forEach((key) => {
      this.addOutput(key, new Classic.Output(socket, key, false))
    })
    this.height =
      100 +
      35 * (Object.keys(this.inputs).length + Object.keys(this.outputs).length)
  }

  async data(inputs: Record<string, any>) {
    const data = await this.module?.exec(inputs)

    return data || {}
  }
}
