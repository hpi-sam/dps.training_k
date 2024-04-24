<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"

	function exerciseStop() {
		socketTrainer.exerciseStop()
	}
</script>

<template>
	<div class="flex-container">
		<h1>Scenario Screen</h1>
		<button class="main-button" @click="exerciseStop">
			Übung beenden
		</button>
	</div>
</template>

<style scoped>
	.main-button {
		background-color: var(--red);
		color: white;
	}
</style>