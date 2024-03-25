<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"
	import { useExerciseStore } from "@/stores/Exercise"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		personnelId: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	function deletePersonnel(){
		socketTrainer.personnelDelete(props.personnelId)
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<h2>{{ exerciseStore.getPersonnel(props.personnelId)?.personnelName }}</h2>
			<button id="deleteButton" @click="deletePersonnel()">
				Personal löschen
			</button>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
	}

	#deleteButton {
		position: relative;
		background-color: #ee4035;
		color: white;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 100%;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}
</style>