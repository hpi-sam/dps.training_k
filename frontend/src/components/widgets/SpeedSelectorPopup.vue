<script setup lang="ts">
	import { ref, watch } from 'vue'
	import CloseButton from './CloseButton.vue'
	import { useExerciseStore } from "@/stores/Exercise"
	import socketTrainer from '@/sockets/SocketTrainer'

	const emit = defineEmits(['close-popup','button-click'])

	const exerciseStore = useExerciseStore()

	const speed = ref(1)

	speed.value = exerciseStore.speed

	watch(() => exerciseStore.speed, () => {
		speed.value = exerciseStore.speed
	})

	function setSpeed(){
		socketTrainer.setSpeed(speed.value)
		emit('close-popup')
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<h2>Geschwindigkeit ändern</h2>
			<br>
			<p>Hier können Sie die Geschwindigkeit der Übung ändern.</p>
			<p>Bei der Geschwindigkeit 2x halbiert sich die Dauer jeder Aktion.</p>
			<br>
			<input
				v-model="speed"
				type="range"
				min="0.2"
				max="4.0"
				step="0.1"
				class="speed-slider"
			>
			<h2>{{ speed }}x</h2>
			<button id="button" @click="setSpeed()">
				Bestätigen
			</button>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		position: relative;
		background-color: white;
		padding: 20px;
		border-radius: 8px;
	}

	h2 {
		margin: 0px 50px;
	}

	#button {
		position: relative;
		border: 1px solid rgb(209, 213, 219);
		background-color: var(--green);
		color: white;
		border-radius: .5rem;
		width: 180px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}

	.speed-slider {
		width: 100%;
	}
</style>