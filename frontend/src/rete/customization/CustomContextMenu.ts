import { BaseSchemes } from 'rete'
import { ContextMenuPlugin, Presets } from 'rete-context-menu-plugin'
import { Items } from 'rete-context-menu-plugin/_types/types'
export { Presets }

export class CustomContextMenu<Schemes extends BaseSchemes> extends ContextMenuPlugin<Schemes> {
    updateItems(newItems: Items<Schemes>) {
        // Uses type assertion to access the private props
        (this as any).props.items = newItems
      }
}
