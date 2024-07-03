import { defineStore } from 'pinia'

export const useTransitionStore = defineStore('transition', {
  state: (): Transitions => ({
    transitions: [],
  }),
  getters: {
    getTransitionById: (state) => {
        return (id: number) => state.transitions.find(transition => transition.id === id)
    },
    getTransitionByNodeId: (state) => {
      return (nodeId: string) => state.transitions.find(transition => transition.nodeId === nodeId)
    }
  },
  actions: {
    addTransition(transition: Transition) {
      this.transitions.push(transition)
    },
    removeTransition(id: number) {
      this.transitions.filter(transition => transition.id !== id)
    },
    updateTransition(id: number, newTransition: Transition) {
      const index = this.transitions.findIndex(transition => transition.id === id)
      this.transitions[index] = newTransition
    },
    clear() {
      this.transitions = []
    }
  }
})