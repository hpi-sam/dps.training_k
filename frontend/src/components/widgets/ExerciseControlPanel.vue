<script setup lang="ts">
	import { svg } from "@/assets/Svg"
	import { ref, computed, watch } from "vue"
	import socketTrainer from "@/sockets/SocketTrainer"
	import { useExerciseStore } from "@/stores/Exercise"

	const exerciseStore = useExerciseStore()

	const status = ref('')
	const speed = ref(1)

	status.value = exerciseStore.status
	speed.value = exerciseStore.speed

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

	function runExercise() {
		if (status.value == "not-started")
			socketTrainer.startExercise()
		else if (status.value == "paused")
			socketTrainer.resumeExercise()
	}

	function pauseExercise() {
		socketTrainer.pauseExercise()
	}

	function endExercise() {
		socketTrainer.endExercise()
	}
</script>
<template>
	<div class="panel">
		<div class="listItemButton">
			<div class="listItemName">
				{{ info }}
			</div>
		</div>
		<div class="rightButtons">
			<button v-if="status != 'ended'" class="speedButton" @click="runExercise">
				{{ speed }}x
			</button>
			<button v-if="status == 'not-started' || status == 'paused'" class="playButton" @click="runExercise">
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
			<button v-if="status == 'running'" class="pauseButton" @click="pauseExercise">
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
			<button v-if="status == 'running' || status == 'paused'" class="endButton" @click="endExercise">
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

	.rightButtons {
		margin-left: auto;
		display: flex;
	}

	.speedButton, .playButton, .pauseButton, .endButton {
		height: 58px;
		width: 60px;
		border: none;
	}

	.playButton {
		background-color: var(--green);
	}

	.pauseButton {
		background-color: var(--yellow);
	}

	.endButton {
		background-color: var(--red);
	}
</style>