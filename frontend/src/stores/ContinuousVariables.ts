import {defineStore} from 'pinia'
import {useExerciseStore} from "@/stores/Exercise"
import {watch} from "vue"
import {ContinuousFunctionName} from "@/enums"
import type {ContinuousState, ContinuousStateInternal, ContinuousVariableInternal} from "@/sockets/MessageData"

let intervalId: number | null = null

export const useContinuousVariablesStore = defineStore('patientContinuous', {
	state: (): ContinuousStateInternal => ({
		timeUntilPhaseChange: Number.NEGATIVE_INFINITY,
		continuousVariables: [],
	}),
	getters: {
		getCurrentValueByName: (state) => {
			return (variableName: string) => {
				const variable = state.continuousVariables.find(v => v.name === variableName)
				return variable ? variable.xCurrent : null
			}
		}
	},
	actions: {
		loadContinuousVariablesFromJSON(continuousState: ContinuousState) {
			this.timeUntilPhaseChange = continuousState.timeUntilPhaseChange

			continuousState.continuousVariables.forEach(variable => {
				const existingVariable = this.continuousVariables.find(v => v.name === variable.name)
				if (existingVariable) {
					existingVariable.xCurrent = variable.current // ToDo: remove
					existingVariable.xStart = existingVariable.xCurrent
					existingVariable.xTarget = variable.target
					existingVariable.tDelta = this.timeUntilPhaseChange
					existingVariable.function = variable.function
					console.log("Continuous Variable overwritten " + existingVariable.name)
				} else this.continuousVariables.push({
					name: variable.name,
					xStart: variable.current,
					xCurrent: variable.current,
					xTarget: variable.target,
					tDelta: this.timeUntilPhaseChange,
					function: variable.function,
				})
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
					variable.xCurrent = this.calculateVariableIncrement(variable)
				})

				this.timeUntilPhaseChange--
			}, 1000)
		},

		calculateVariableIncrement(variable: ContinuousVariableInternal) {
			console.log("Time until phase change: " + this.timeUntilPhaseChange)
			switch (variable.function) {
				case ContinuousFunctionName.LINEAR:
					return variable.xCurrent + linear(variable, this.timeUntilPhaseChange)
				case ContinuousFunctionName.INCREMENT:
					return variable.xCurrent + 1
				case ContinuousFunctionName.DECREMENT:
					return variable.xCurrent - 1
				default:
					console.error("Unrecognized function: " + variable.function)
					return variable.xCurrent
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

function linear(variable: ContinuousVariableInternal, timeUntilPhaseChange: number) {
	return ((variable.xTarget - variable.xCurrent) / timeUntilPhaseChange)
}
