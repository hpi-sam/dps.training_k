import { NodeEditor } from "rete";
import { AreaPlugin } from "rete-area-plugin";
import { DataflowEngine } from "rete-engine";
import { Schemes } from "./modules";
import { AddNode } from "./nodes/add";

export function createEngine<S extends Schemes>(
  editor: NodeEditor<S>,
  area: AreaPlugin<S, any>
) {
  const dataflow = new DataflowEngine<S>();

  async function process() {
    dataflow.reset();
    for (const node of editor.getNodes()) {
      if (node instanceof AddNode) {
        try {
          await dataflow.fetch(node.id);

          area.update("control", node.controls["result"].id);
        } catch (e) {
          // prevent full-screen error
          console.error(e);
        }
      }
    }
  }
  editor.addPipe((context) => {
    if (["connectioncreated", "connectionremoved"].includes(context.type)) {
      process();
    }
    return context;
  });

  return {
    dataflow,
    process
  };
}
