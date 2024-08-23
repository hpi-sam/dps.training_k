import { GetSchemes, NodeEditor } from "rete"
import { InputNode } from "./nodes/input"
import { OutputNode } from "./nodes/output"
import { DataflowEngine  } from "rete-engine"

export type Schemes = GetSchemes<any, any>;

export type Module<S extends Schemes> = {
  apply: (editor: NodeEditor<S>) => Promise<void>;
  exec: (data: Record<string, any>) => Promise<any>;
};

export class Modules<S extends Schemes> {
  constructor(
    private has: (id: string) => boolean,
    private graph: (id: string, editor: NodeEditor<S>) => Promise<void>
  ) {}

  public findModule = (id: string): null | Module<S> => {
    //if (!this.has(id)) return null

    return {
      apply: (editor: NodeEditor<S>) => this.graph(id, editor),
      exec: async (inputData: Record<string, any>) => {
        const engine = new DataflowEngine<S>()
        const editor = new NodeEditor<S>()

        editor.use(engine)

        await this.graph(id, editor)

        return this.execute(inputData, editor, engine)
      }
    }
  }

  private async execute(
    inputs: Record<string, any>,
    editor: NodeEditor<S>,
    engine: DataflowEngine<S>
  ) {
    const nodes = editor.getNodes()

    this.injectInputs(nodes, inputs)

    return this.retrieveOutputs(nodes, engine)
  }

  private injectInputs(nodes: S["Node"][], inputData: Record<string, any>) {
    const inputNodes = nodes.filter(
      (node): node is InputNode => node instanceof InputNode
    )

    inputNodes.forEach((node) => {
      const key = node.controls.key.value
      if (key) {
        node.key = inputData[key] && inputData[key][0]
      }
    })
  }

  private async retrieveOutputs(nodes: S["Node"][], engine: DataflowEngine<S>) {
    const outputNodes = nodes.filter(
      (node): node is OutputNode => node instanceof OutputNode
    )
    const outputs = await Promise.all(
      outputNodes.map(async (outNode) => {
        const data = await engine.fetchInputs(outNode.id)

        return [outNode.controls.key.value || "", data.value[0]] as const
      })
    )

    return Object.fromEntries(outputs)
  }

  public static getPorts(editor: NodeEditor<Schemes>) {
    const nodes = editor.getNodes()
    const inputs = nodes
      .filter((n): n is InputNode => n instanceof InputNode)
      .map((n) => n.controls.key.value as string)
    const outputs = nodes
      .filter((n): n is OutputNode => n instanceof OutputNode)
      .map((n) => n.controls.key.value as string)

    return {
      inputs,
      outputs
    }
  }
}
