import { ClassicPreset as Classic } from "rete"

export interface DropdownOption {
    name: string;
    value: string;
  }
  
  export class DropdownControl extends Classic.Control {
    private _selection: DropdownOption
    optionsList: DropdownOption[]
    onChange: (option: DropdownOption) => void
  
    constructor(optionsList: DropdownOption[], initial?: DropdownOption, change?: (option: DropdownOption) => void) {
      super()
      this.optionsList = optionsList || []
      this._selection = initial || this.optionsList[0]
      this.onChange = change as any
    }

    get selection(): DropdownOption {
      return this._selection
    }

    set selection(option: DropdownOption) {
      this._selection = option    
      this.onChange(option)
    }
  }