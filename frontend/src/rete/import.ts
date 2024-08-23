import { Connection, Context } from "./types"
import {
  InputNode,
  OutputNode,
  StateNode,
  ActionNode,
  TransitionNode
} from "./nodes/index"
import { removeConnections } from "./utils"
import { ActionIDs } from "./constants"
import { DropdownOption } from "./dropdown"
import { addState } from "@/components/ModulePatientEditor.vue"

export async function createNode(
  { editor, area, process, transitionModulesData, transitionModules, componentModulesData, componentModules }: Context,
  type: string,
  data: any
) {
  if (type === "Input") return new InputNode(data?.key)
  if (type === "Output") return new OutputNode(data?.key)
  if (type === "Transition") {
    const transitionNode = new TransitionNode(
      transitionModulesData,
      transitionModules.findModule,
      (id) => removeConnections(editor, id),
      async (id) => {
        area.update("node", id)
        process()
      }
    )
    await transitionNode.update()
    return transitionNode
  }
  if (type === "State") {
    const stateNode = new StateNode()
    addState(stateNode.id)
    return stateNode
  }
  if (type === "Action") return new ActionNode()
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
    } else if (n.type === "State") {
      const node = new StateNode()
      node.id = n.id
      await context.editor.addNode(node)
    } else if (n.type === "Input") {
      const node = new InputNode(n.key)
      node.id = n.id
      await context.editor.addNode(node)
    } else if (n.type === "Output") {
      const node = new OutputNode(n.key)
      node.id = n.id
      await context.editor.addNode(node)
    } else if (n.type === "Transition") {
      const node = new TransitionNode(
        context.transitionModulesData,
        context.transitionModules.findModule,
        (id) => removeConnections(context.editor, id),
        async (id) => {
          context.area.update("node", id)
          context.process()
        },
        {
          name: n.transition,
          value: n.transition,
        }
      )
      node.id = n.id
      await node.update()
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
    
    if (n.type === "State" || n.type === "Transition") {
      const source = context.editor.getNode(n.id)
      const target = context.editor.getNode(n.next)
      createConnection(source, "next", target, "in", context)
    }

    if (n.type === "Input") {
      const source = context.editor.getNode(n.id)
      const target = context.editor.getNode(n.next)
      createConnection(source, "out", target, "in", context)
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
  } else {
    //throw new Error("Invalid connection:" + [source?.id, sourceOutput, target?.id, targetInput])
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

    if (n.label === "State" && n instanceof StateNode) {
      nodes.push({
        id: n.id,
        type: n.label,
        next: connections.filter(c => c.source === n.id)[0]?.target || null,
      })
    }

    if (n.label === "Transition" && n instanceof TransitionNode) {
      nodes.push({
        id: n.id,
        type: n.label,
        transition: n.controls.selection.selection.name,
        next: connections.filter(c => c.source === n.id)[0]?.target || null,
      })
    }

    if (n.label === "Input" && n instanceof InputNode) {
      nodes.push({
        id: n.id,
        type: n.label,
        key: n.data().key,
        next: connections.filter(c => c.source === n.id)[0]?.target || null,
      })
    }

    if (n.label === "Output" && n instanceof OutputNode) {
      nodes.push({
        id: n.id,
        type: n.label,
        key: n.data().key,
      })
    }
  }

  return nodes
}