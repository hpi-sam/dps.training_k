<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		areaName: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	function deleteArea(){
		socketTrainer.areaDelete(props.areaName as string)
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<h2>{{ props.areaName }}</h2>
			<button id="deleteButton" @click="deleteArea()">
				Bereich löschen
			</button>
		</div>
	</div>
</template>

<style scoped>
	.popup-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;
		z-index: 1;
	}

	.popup {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
	}

	.button-container {
		margin-top: 10px;
		display: flex;
		justify-content: center;
	}

	.button-container > button {
		width: 50px;
		height: 50px;
		margin: 10px;
	}

	#deleteButton {
		position: relative;
		background-color: red;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		box-sizing: border-box;
		display: flex;
		align-items: center;
		width: 100%;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}

	.areaButtons:hover, #addAreaButton:hover {
		background-color: rgb(249, 250, 251);
	}

	.areaButtons:active, #addAreaButton:active {
		background-color: rgb(243, 244, 246);
	}
</style>