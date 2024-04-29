<script setup lang="ts">
	import { svg } from "@/assets/Svg"
	import { ref, computed, watch } from "vue"
	import socketTrainer from "@/sockets/SocketTrainer"
	import { useExerciseStore } from "@/stores/Exercise"
	import ButtonPopup from "./ButtonPopup.vue"
	import SpeedSelectorPopup from "./SpeedSelectorPopup.vue"
	import { useAvailablesStore } from "@/stores/Availables"
	import { useLogStore } from "@/stores/Log"
	import {Screens, setLeftScreen, setRightScreen} from "@/components/ModuleTrainer.vue"

	const exerciseStore = useExerciseStore()

	const status = ref('')
	const speed = ref(1)

	status.value = exerciseStore.status
	speed.value = exerciseStore.speed

	watch(() => exerciseStore.status, () => {
		status.value = exerciseStore.status
	})

	watch(() => exerciseStore.speed, () => {
		speed.value = exerciseStore.speed
	})

	const info = computed(() => {
		switch (status.value) {
			case "not-started":
				return "Die Übung wurde noch nicht gestartet"
			case "running":
				return "Die Übung läuft"
			case "paused":
				return "Die Übung ist pausiert"
			case "ended":
				return "Die Übung ist beendet"
			default:
				return "Fehler"
		}
	})

	function leaveExercise() {
		useAvailablesStore().$reset()
		useExerciseStore().$reset()
		useLogStore().$reset()
		setLeftScreen(Screens.CREATE_EXERCISE)
		setRightScreen(Screens.JOIN_EXERCISE)
	}

	function startExercise() {
		socketTrainer.exerciseStart()
	}

	function resumeExercise() {
		socketTrainer.exerciseResume()
	}

	function pauseExercise() {
		socketTrainer.exercisePause()
	}

	function endExercise() {
		socketTrainer.exerciseEnd()
	}

	const showLeavePopup = ref(false)
	const showSpeedPopup = ref(false)
	const showStartPopup = ref(false)
	const showPausePopup = ref(false)
	const showResumePopup = ref(false)
	const showEndPopup = ref(false)
</script>
<template>
	<SpeedSelectorPopup
		v-if="showSpeedPopup"
		@close-popup="showSpeedPopup = false"
	/>
	<ButtonPopup
		v-if="showStartPopup"
		title="Möchten Sie die Übung starten?"
		button-text="Starten"
		button-color="var(--green)"
		button-text-color="white"
		@button-click="startExercise"
		@close-popup="showStartPopup = false"
	/>
	<ButtonPopup
		v-if="showPausePopup"
		title="Möchten Sie die Übung pausieren?"
		button-text="Pausieren"
		button-color="var(--yellow)"
		button-text-color="white"
		@button-click="pauseExercise"
		@close-popup="showPausePopup = false"
	/>
	<ButtonPopup
		v-if="showResumePopup"
		title="Möchten Sie die Übung fortsetzen?"
		button-text="Fortsetzen"
		button-color="var(--green)"
		button-text-color="white"
		@button-click="resumeExercise"
		@close-popup="showResumePopup = false"
	/>
	<ButtonPopup
		v-if="showEndPopup"
		title="Möchten Sie die Übung beenden?"
		button-text="Beenden"
		button-color="var(--red)"
		button-text-color="white"
		@button-click="endExercise"
		@close-popup="showEndPopup = false"
	/>
	<ButtonPopup
		v-if="showLeavePopup"
		title="Möchten Sie die Übung verlassen?"
		button-text="Verlassen"
		button-color="var(--red)"
		button-text-color="white"
		@button-click="leaveExercise"
		@close-popup="showLeavePopup = false"
	/>
	<div class="panel">
		<button
			class="leaveButton"
			@click="showLeavePopup = true"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				height="24"
				viewBox="0 -960 960 960"
				width="24"
				fill="white"
			>
				<path :d="svg.arrowBackIcon" />
			</svg>
		</button>
		<div class="listItemButton">
			<div class="listItemName">
				{{ info }}
			</div>
		</div>
		<div class="rightButtons">
			<button
				v-if="status != 'ended'"
				class="speedButton"
				@click="showSpeedPopup = true"
			>
				{{ speed }}x
			</button>
			<button
				v-if="status == 'not-started'"
				class="startButton"
				@click="showStartPopup = true"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24"
					viewBox="0 -960 960 960"
					width="24"
					fill="white"
				>
					<path :d="svg.playIcon" />
				</svg>
			</button>
			<button
				v-if="status == 'paused'"
				class="startButton"
				@click="showResumePopup = true"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24"
					viewBox="0 -960 960 960"
					width="24"
					fill="white"
				>
					<path :d="svg.playIcon" />
				</svg>
			</button>
			<button
				v-if="status == 'running'"
				class="pauseButton"
				@click="showPausePopup = true"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24"
					viewBox="0 -960 960 960"
					width="24"
					fill="white"
				>
					<path :d="svg.pauseIcon" />
				</svg>
			</button>
			<button
				v-if="status == 'running' || status == 'paused'"
				class="endButton"
				@click="showEndPopup = true"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					height="24"
					viewBox="0 -960 960 960"
					width="24"
					fill="white"
				>
					<path :d="svg.closeIcon" />
				</svg>
			</button>
		</div>
	</div>
</template>
<style scoped>
	.panel {
		position: absolute;
		bottom: 0rem;
		width: 100%;
		background-color: white;
		border-top: 2px solid var(--border-color);
		display: flex;
		align-items: center;
	}

	.listItemButton {
		flex-grow: 1;
		height: 100%;
	}

	.leaveButton {
		background-color: var(--red);
	}

	.rightButtons {
		margin-left: auto;
		display: flex;
	}

	.leaveButton, .speedButton, .startButton, .pauseButton, .endButton {
		height: 58px;
		width: 60px;
		border: none;
	}

	.speedButton {
		font-size: 1.25rem;
		line-height: 1.25rem;
	}

	.startButton {
		background-color: var(--green);
	}

	.pauseButton {
		background-color: var(--yellow);
	}

	.endButton {
		background-color: var(--red);
	}
</style>