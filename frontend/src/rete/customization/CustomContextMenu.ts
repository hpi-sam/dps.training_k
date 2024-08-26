import { BaseSchemes, Scope } from 'rete'
import { ContextMenuPlugin, Presets } from 'rete-context-menu-plugin'
import { Item, Items, Position } from 'rete-context-menu-plugin/_types/types'
export { Presets }

export class CustomContextMenu<Schemes extends BaseSchemes> extends ContextMenuPlugin<Schemes> {
    updateItems(newItems: Items<Schemes>) {
        // Use type assertion to access the private props
        (this as any).props.items = newItems
      }
}
