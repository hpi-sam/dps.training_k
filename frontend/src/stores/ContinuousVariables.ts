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
				case ContinuousFunctionName.SIGMOID:
					// console.log("Calculate sigmoid: " + (variable.xCurrent + sigmoid(variable, this.timeUntilPhaseChange)) + "; Time until phase" +
					// 	" change: " + this.timeUntilPhaseChange)
					return variable.xCurrent + sigmoid(variable, this.timeUntilPhaseChange)
				case ContinuousFunctionName.SIGMOID_DELAYED:
					return variable.xCurrent + sigmoid_delayed(variable, this.timeUntilPhaseChange)
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

function sigmoid(variable: ContinuousVariableInternal, timeUntilPhaseChange: number): number {
	// higher value = steeper; higher -> lower infinTargetCorrection
	const steepness = 10
	// magic value (try & error for steepness 10/20) needed for correction as the target height is only reached -> infin
	const infinTargetCorrection = 3.5

	const t = variable.tDelta - timeUntilPhaseChange
	const tMid = variable.tDelta / 2

	const tStretchFactor = 1 / ((Math.pow(variable.tDelta, 2)) / Math.pow(steepness, 2))
	const tStretchCorrectorNormalizer = Math.atan(Math.sqrt(1) * variable.tDelta) / Math.sqrt(1)
	const tStretchCorrector = (Math.atan(Math.sqrt(tStretchFactor) * variable.tDelta) / Math.sqrt(tStretchFactor)) / tStretchCorrectorNormalizer

	// original height of atanDerivative fun, - infinTargetCorrection scaled with t_delta
	const pi = Math.PI - (infinTargetCorrection / variable.tDelta)
	const xDelta = variable.xTarget - variable.xStart
	const xStretcher = xDelta / pi

	const atanDerivative = (1 / (Math.pow(t - tMid, 2) * tStretchFactor + 1))

	return atanDerivative * xStretcher / tStretchCorrector
}

function sigmoid_delayed(variable: ContinuousVariableInternal, timeUntilPhaseChange: number): number {
	// higher value = steeper; higher -> lower infinTargetCorrection
	const steepness = 10
	// magic value (try & error for steepness 10/20) needed for correction as the target height is only reached -> infin
	const infinTargetCorrection = 3.5

	const t = variable.tDelta - timeUntilPhaseChange
	const tMid = variable.tDelta / 2

	const tShiftFrac = 3
	const t0Shifted = variable.tDelta / tShiftFrac  // Time when sigmoid starts (shifted by one tShiftFrac)
	const tDeltaShifted = variable.tDelta - t0Shifted
	const tShiftedMid = tMid + (variable.tDelta - tMid) / tShiftFrac  // Shifted midpoint

	const tStretchFactor = 1 / ((Math.pow(tDeltaShifted, 2)) / Math.pow(steepness, 2))
	const tStretchCorrectorNormalizer = Math.atan(Math.sqrt(1) * variable.tDelta) / Math.sqrt(1)
	const tStretchCorrector = (Math.atan(Math.sqrt(tStretchFactor) * variable.tDelta) / Math.sqrt(tStretchFactor)) / tStretchCorrectorNormalizer

	// original height of atanDerivative fun, - infinTargetCorrection scaled with t_delta
	const pi = Math.PI - (infinTargetCorrection / tDeltaShifted)
	const xDelta = variable.xTarget - variable.xStart
	const xStretcher = xDelta / pi

	const atanDerivative = (1 / (Math.pow(t - tShiftedMid, 2) * tStretchFactor + 1))

	if (t < t0Shifted) {
		console.log("straight")
		return 0
	} else return atanDerivative * xStretcher / tStretchCorrector
}