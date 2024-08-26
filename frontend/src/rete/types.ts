import { ClassicPreset as Classic, GetSchemes, NodeEditor } from 'rete'
import { Modules } from "./modules.js"
import { Area2D, AreaPlugin } from 'rete-area-plugin'
import { VueArea2D } from 'rete-vue-plugin'
import { ContextMenuExtra } from 'rete-context-menu-plugin'

import {
    InputNode,
    OutputNode,
    StateNode,
    ActionNode,
    TransitionNode,
    InitialStateNode
  } from "./nodes/index.js"

export type Node = StateNode | InputNode | OutputNode | ActionNode | TransitionNode | InitialStateNode

export class Connection<A extends Node, B extends Node> extends Classic.Connection<A,B> {}

export type Conn =
  | Connection<InputNode, OutputNode>
  | Connection<InputNode, ActionNode>
  | Connection<ActionNode, OutputNode>
  | Connection<ActionNode, ActionNode>
  | Connection<StateNode, TransitionNode>
  | Connection<TransitionNode, StateNode>

export type Schemes = GetSchemes<Node, Conn>

export type AreaExtra =
  | Area2D<Schemes>
  | VueArea2D<Schemes>
  | ContextMenuExtra

export type Context = {
    editor: NodeEditor<Schemes>
    area: AreaPlugin<Schemes, any>
    transitionModulesData: any
    transitionModules: Modules<Schemes>
    componentModulesData: any
    componentModules: Modules<Schemes>
}

export interface Editor {
    getModules(): { patientModuleData: string, transitionModulesData: string[], componentModulesData: string[] };
    saveModule(): void;
    restoreModule(): void;
    newTransitionModule(id: string): void;
    newComponentModule(id: string): void;
    openModule(id: string, type: string): Promise<void>;
    layout(): Promise<void>;
    destroy(): void;
}

export interface State {
    id: string;
    airway: string;
    breathingRate: number;
    oxygenSaturation: number;
    breathing: string;
    breathingSound: boolean;
    breathingLoudness: string;
    heartRate: number;
    pulsePalpable: string;
    rivaRocci: string;
    consciousness: string;
    pupils: string;
    psyche: string;
    skinFining: string;
    skinDiscoloration: string;
    bgaOxy: number;
    bgaSbh: number;
    hb: number;
    bz: number;
    clotting: number;
    liver: number;
    kidney: number;
    infarct: number;
    lactate: number;
    extremities: number;
    thorax: number;
    trauma: number;
    ultraschall: number;
    ekg: number;
    zvd: number;
}