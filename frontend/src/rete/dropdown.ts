import { ClassicPreset as Classic } from "rete"

export interface DropdownOption {
    name: string;
    value: string;
  }
  
  export class DropdownControl extends Classic.Control {
    selection: DropdownOption
    optionsList: DropdownOption[]
  
    constructor(optionsList: DropdownOption[], initial?: DropdownOption, change?: (option: DropdownOption) => void) {
      super()
      this.optionsList = optionsList || []
      this.selection = initial || this.optionsList[0]
      this.onChange = change as any
    }
  
    setValue(option: DropdownOption): void {
      this.selection = option
      if (this.onChange) {
        this.onChange(option)
      }
    }
  
    onChange(option: DropdownOption): void {
      this.setValue(option)
    }
  }