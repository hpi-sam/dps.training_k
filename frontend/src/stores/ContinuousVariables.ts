import {defineStore} from 'pinia'
import {useExerciseStore} from "@/stores/Exercise"
import {watch} from "vue"
import {ContinuousFunctionName} from "@/enums"
import type {ContinuousState, ContinuousStateInternal, ContinuousVariableInternal} from "@/sockets/MessageData"

let intervalId: number | null = null

export const useContinuousVariablesStore = defineStore('patientContinuous', {
	state: (): ContinuousState => ({
		timeUntilPhaseChange: Number.NEGATIVE_INFINITY,
		continuousVariables: [],
	}),
	getters: {
		getCurrentValueByName: (state) => {
			return (variableName: string) => {
				const variable = state.continuousVariables.find(v => v.name === variableName)
				return variable ? variable.current : null
			}
		}
	},
	actions: {
		loadContinuousVariablesFromJSON(continuousState: ContinuousState) {
			this.timeUntilPhaseChange = continuousState.timeUntilPhaseChange

			continuousState.continuousVariables.forEach(variable => {
				const existingVariable = this.continuousVariables.find(v => v.name === variable.name)
				if (existingVariable) {
					existingVariable.target = variable.target
					existingVariable.function = variable.function
				} else this.continuousVariables.push(variable)
			})

			if (useExerciseStore().status == "running") startContinuousLogic()
		},

		startUpdatingContinuousVariables() {
			if (intervalId !== null) return

			intervalId = setInterval(() => {
				if (this.timeUntilPhaseChange <= 0) {
					this.stopUpdatingContinuousVariables()
					return
				}
				this.continuousVariables.forEach(variable => {
					variable.current = this.calculateVariableIncrement(variable)
				})

				this.timeUntilPhaseChange--
			}, 1000)
		},

		calculateVariableIncrement(variable: ContinuousVariable) {
			switch (variable.function) {
				case "linear":
					return variable.current + ((variable.target - variable.current) / this.timeUntilPhaseChange)
				case "increment":
					return variable.current + 1
				case "decrement":
					return variable.current - 1
				default:
					console.error("Unrecognized function: " + variable.function)
					return variable.current
			}
		},

		stopUpdatingContinuousVariables() {
			this.timeUntilPhaseChange = 0
			if (intervalId !== null) {
				clearInterval(intervalId)
				intervalId = null
			}
		}
	}
})

export function startContinuousLogic() {
	const patientStore = useContinuousVariablesStore()
	const exerciseStore = useExerciseStore()

	watch(
		() => exerciseStore.status,
		(newVal) => {
			if (newVal === "running") {
				patientStore.startUpdatingContinuousVariables()
			} else {
				patientStore.stopUpdatingContinuousVariables()
			}
		},
		{immediate: true}
	)
}
