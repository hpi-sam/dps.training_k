import { defineStore } from 'pinia'

export const useTransitionStore = defineStore('transition', {
    state: (): { transitions: Record<number, Transition> } => ({
        transitions: {},
    }),
    actions: {
        getTransition(id: number) {
            return this.transitions[id]
        },
        addTransition(transition: Transition) {
            this.transitions[transition.id] = transition
        },
        removeTransition(id: number) {
            delete this.transitions[id]
        },
        updateTransition(id: number, newTransition: Transition) {
            this.transitions[id] = newTransition
        },
    }
})