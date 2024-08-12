import { Connection, Context } from "./types"
import {
  AddNode,
  InputNode,
  ModuleNode,
  NumberNode,
  OutputNode,
  StateNode,
  isTrueNode
} from "./nodes"
import { removeConnections } from "./utils"

export async function createNode(
  { editor, area, dataflow, modules, process }: Context,
  name: string,
  data: any
) {
  if (name === "Number") return new NumberNode(data.value, process)
  if (name === "Add") return new AddNode(process, data)
  if (name === "Input") return new InputNode(data.key)
  if (name === "Output") return new OutputNode(data.key)
  if (name === "Module") {
    const node = new ModuleNode(
      data.name,
      modules.findModule,
      (id) => removeConnections(editor, id),
      (id) => {
        area.update("node", id)
        process()
      }
    )
    await node.update()

    return node
  }
  if (name === "State") return new StateNode()
  if (name === "isTrue") return new isTrueNode()
  throw new Error("Unsupported node")
}

export async function importEditor(context: Context, data: any) {
  const { nodes, connections } = data

  for (const n of nodes) {
    const node = await createNode(context, n.name, n.data)
    node.id = n.id
    await context.editor.addNode(node)
  }
  for (const c of connections) {
    const source = context.editor.getNode(c.source)
    const target = context.editor.getNode(c.target)

    if (
      source &&
      target &&
      (source.outputs as any)[c.sourceOutput] &&
      (target.inputs as any)[c.targetInput]
    ) {
      const conn = new Connection(
        source,
        c.sourceOutput as never,
        target,
        c.targetInput as never
      )

      await context.editor.addConnection(conn)
    }
  }
}

export function exportEditor(context: Context) {
  const nodes = []
  const connections = []

  for (const n of context.editor.getNodes()) {
    nodes.push({
      id: n.id,
      name: n.label,
      data: n.serialize()
    })
  }
  for (const c of context.editor.getConnections()) {
    connections.push({
      source: c.source,
      sourceOutput: c.sourceOutput,
      target: c.target,
      targetInput: c.targetInput
    })
  }

  return {
    nodes,
    connections
  }
}
