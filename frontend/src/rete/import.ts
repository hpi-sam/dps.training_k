import { Connection, Context } from "./types"
import {
  AddNode,
  InputNode,
  ModuleNode,
  NumberNode,
  OutputNode,
  StateNode,
  ActionNode,
  isInRangeNode
} from "./nodes/index"
import { removeConnections } from "./utils"
import { ActionIDs } from "./constants"
import { DropdownOption } from "./dropdown"

export async function createNode(
  { editor, area, dataflow, modules, process }: Context,
  type: string,
  data: any
) {
  if (type === "Number") return new NumberNode(data.value, process)
  if (type === "Add") return new AddNode(process, data)
  if (type === "Input") return new InputNode(data.key)
  if (type === "Output") return new OutputNode(data.key)
  if (type === "Module") {
    const node = new ModuleNode(
      data.type,
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
  if (type === "State") return new StateNode()
  if (type === "Action") return new ActionNode()
  if (type === "isInRange") return new isInRangeNode(data.fromValue, data.toValue)
  throw new Error("Unsupported node")
}

export async function importEditor(context: Context, nodes: any) {
  for (const n of nodes) {
    if (n.type === "Action") {
      let initialSelection: DropdownOption = {
        name: "",
        value: "",
      }
      ActionIDs.find((action) => {
        if (action.id === n.action) {
          initialSelection = {
            name: action.name,
            value: action.id,
          }
        }
      })
      const node = new ActionNode(initialSelection, undefined, n.quantity)
      node.id = n.id
      await context.editor.addNode(node)
    } else { 
      const node = await createNode(context, n.type, n.data)
      node.id = n.id
      await context.editor.addNode(node)
    }
  }

  for (const n of nodes) {
    if (n.type === "Action") {
      const source = context.editor.getNode(n.id)
      const target1 = context.editor.getNode(n.next.true)
      const target2 = context.editor.getNode(n.next.false)
      createConnection(source, "true", target1, "in", context)
      createConnection(source, "false", target2, "in", context)
    }
    
    if (n.type === "State" || n.type === "Transition" || n.type === "Input") {
      const source = context.editor.getNode(n.id)
      const target = context.editor.getNode(n.next)
      createConnection(source, "next", target, "in", context)
    }
  }
}

async function createConnection(source: any, sourceOutput: any, target: any, targetInput: any, context: Context) {
  if (
    source &&
    target &&
    (source.outputs as any)[sourceOutput] &&
    (target.inputs as any)[targetInput]
  ) {
    const conn = new Connection(
      source,
      sourceOutput as never,
      target,
      targetInput as never
    )

    await context.editor.addConnection(conn)
  }
}

export function exportEditor(context: Context) {
  const nodes = []
  const connections = context.editor.getConnections()

  for (const n of context.editor.getNodes()) {
    if (n.label === "Action" && n instanceof ActionNode) {
      nodes.push({
        id: n.id,
        type: n.label,
        action: n.selection().value,
        quantity: n.quantity(),
        next: {
          true: connections.filter(c => c.source === n.id && c.sourceOutput === "true")[0]?.target || null,
          false: connections.filter(c => c.source === n.id && c.sourceOutput === "false")[0]?.target || null,
        }
      })
    }

    if (n.label === "State" || n.label === "Transition" || n.label === "Input") {
      nodes.push({
        id: n.id,
        type: n.label,
        //next: n.outputs.get("out").connections[0].input.node.id
      })
    }
  }

  return nodes
}