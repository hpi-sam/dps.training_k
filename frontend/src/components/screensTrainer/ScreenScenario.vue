<script setup lang="ts">
	import ButtonMainAction from "@/components/widgets/ButtonMainAction.vue"
	import socketTrainer from "@/sockets/SocketTrainer"

	function exerciseStop() {
		socketTrainer.exerciseStop()
	}
</script>

<template>
	Scenario Screen
	<ButtonMainAction
		:button-text="'Übung beenden'"
		@on-pressed="exerciseStop"
	/>
</template>