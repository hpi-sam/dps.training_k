<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"

	function exerciseStop() {
		socketTrainer.exerciseStop()
	}
</script>

<template>
	<div class="flex-container">
		Scenario Screen
		<button class="main-button" @click="exerciseStop">
			Übung beenden
		</button>
	</div>
</template>