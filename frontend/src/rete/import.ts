import { Connection, Context } from "./types"
import {
  InputNode,
  OutputNode,
  StateNode,
  ActionNode,
  TransitionNode,
  InitialStateNode,
  ComponentNode,
  MaterialNode
} from "./nodes/index"
import { removeConnections } from "./utils"
import { ActionIDs, MaterialIDs } from "./constants"
import { DropdownOption } from "./dropdown"
import { addState } from '@/components/screensTrainer/ScreenPatientEditor.vue'

export async function createNode(
  { editor, area, transitionModulesData, transitionModules, componentModulesData, componentModules }: Context,
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
      async (id) => area.update("node", id)
    )
    await transitionNode.update()
    return transitionNode
  }
  if (type === "State") {
    const stateNode = new StateNode()
    addState(stateNode.id)
    return stateNode
  }
  if (type === "InitialState") {
    const initialStateNode = new InitialStateNode()
    addState(initialStateNode.id)
    return initialStateNode
  }
  if (type === "Action") return new ActionNode()
  if (type === "Material") return new MaterialNode()
  if (type === "Component") {
    const componentNode = new ComponentNode(
      componentModulesData,
      componentModules.findModule,
      (id) => removeConnections(editor, id),
      async (id) => area.update("node", id)
    )
    await componentNode.update()
    return componentNode
  }
  throw new Error("Unsupported node")
}

export async function importEditor(context: Context, nodes: any) {
  // Import nodes
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
    }

    if (n.type === "Material") {
      let initialSelection: DropdownOption = {
        name: "",
        value: "",
      }
      MaterialIDs.find((material) => {
        if (material.id === n.material) {
          initialSelection = {
            name: material.name,
            value: material.id,
          }
        }
      })
      const node = new MaterialNode(initialSelection, undefined, n.quantity)
      node.id = n.id
      await context.editor.addNode(node)
    }

    if (n.type === "InitialState") {
      const node = new InitialStateNode()
      node.id = n.id
      await context.editor.addNode(node)
    }
    if (n.type === "State") {
      const node = new StateNode()
      node.id = n.id
      await context.editor.addNode(node)
    }
    if (n.type === "Input") {
      const node = new InputNode(n.key)
      node.id = n.id
      await context.editor.addNode(node)
    }
    if (n.type === "Output") {
      const node = new OutputNode(n.key)
      node.id = n.id
      await context.editor.addNode(node)
    }
    if (n.type === "Transition") {
      const node = new TransitionNode(
        context.transitionModulesData,
        context.transitionModules.findModule,
        (id) => removeConnections(context.editor, id),
        async (id) => context.area.update("node", id),
        {
          name: n.transition,
          value: n.transition,
        }
      )
      node.id = n.id
      await node.update()
      await context.editor.addNode(node)
    }
    if (n.type === "Component") {
      const node = new ComponentNode(
        context.componentModulesData,
        context.componentModules.findModule,
        (id) => removeConnections(context.editor, id),
        async (id) => context.area.update("node", id),
        {
          name: n.component,
          value: n.component,
        }
      )
      node.id = n.id
      await node.update()
      await context.editor.addNode(node)
    }
  }

  // Import connections
  for (const n of nodes) {
    if (n.type === "Action" || n.type === "Material") {
      const source = context.editor.getNode(n.id)
      const target1 = context.editor.getNode(n.next.true)
      const target2 = context.editor.getNode(n.next.false)
      createConnection(source, "true", target1, "in", context)
      createConnection(source, "false", target2, "in", context)
    }
    
    if (n.type === "State" || n.type === "InitialState") {
      const source = context.editor.getNode(n.id)
      const target = context.editor.getNode(n.next)
      createConnection(source, "next", target, "in", context)
    }
    
    if (n.type === "Transition" || n.type === "Component") {
      const source = context.editor.getNode(n.id)

      for (const next of n.next) {
        const target = context.editor.getNode(next.value)
        createConnection(source, next.key, target, "in", context)
      }
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
  }
}

export function exportEditor(context: Context) {
  const nodes = []
  const connections = context.editor.getConnections()

  for (const n of context.editor.getNodes()) {
    if (n instanceof ActionNode) {
      nodes.push({
        id: n.id,
        type: 'Action',
        action: n.selection().value,
        quantity: n.quantity(),
        next: {
          true: connections.filter(c => c.source === n.id && c.sourceOutput === "true")[0]?.target || null,
          false: connections.filter(c => c.source === n.id && c.sourceOutput === "false")[0]?.target || null,
        }
      })
    }

    if (n instanceof MaterialNode) {
      nodes.push({
        id: n.id,
        type: 'Material',
        material: n.selection().value,
        quantity: n.quantity(),
        next: {
          true: connections.filter(c => c.source === n.id && c.sourceOutput === "true")[0]?.target || null,
          false: connections.filter(c => c.source === n.id && c.sourceOutput === "false")[0]?.target || null,
        }
      })
    }

    if (n instanceof StateNode) {
      nodes.push({
        id: n.id,
        type: 'State',
        next: connections.filter(c => c.source === n.id)[0]?.target || null,
      })
    }

    if (n instanceof InitialStateNode) {
      nodes.push({
        id: n.id,
        type: 'InitialState',
        next: connections.filter(c => c.source === n.id)[0]?.target || null,
      })
    }

    if (n instanceof TransitionNode) {
      const nextList = []
      const outgoingConnections = connections.filter(c => c.source === n.id)
      for (const o of outgoingConnections) {
        nextList.push({
          key: o.sourceOutput,
          value: o.target
        })
      }

      nodes.push({
        id: n.id,
        type: 'Transition',
        transition: n.controls.selection.selection.name,
        next: nextList
      })
    }

    if (n instanceof ComponentNode) {
      const nextList = []
      const outgoingConnections = connections.filter(c => c.source === n.id)
      for (const o of outgoingConnections) {
        nextList.push({
          key: o.sourceOutput,
          value: o.target
        })
      }

      nodes.push({
        id: n.id,
        type: 'Component',
        component: n.controls.selection.selection.name,
        next: nextList
      })
    }

    if (n instanceof InputNode) {
      nodes.push({
        id: n.id,
        type: 'Input',
        key: n.data().key,
        next: connections.filter(c => c.source === n.id)[0]?.target || null,
      })
    }

    if (n instanceof OutputNode) {
      nodes.push({
        id: n.id,
        type: 'Output',
        key: n.data().key,
      })
    }
  }

  return nodes
}