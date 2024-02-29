<script setup lang="ts">
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import ButtonMainAction from "@/components/widgets/ButtonMainAction.vue"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"

	const exerciseStore = useExerciseStore()

	function exerciseStart() {
		socketTrainer.exerciseStart()
	}
</script>

<template>
	<TopBarTrainer />
	<div>Geladenes Übungsobjekt: <br>{{ exerciseStore }}</div>
	<ButtonMainAction
		:button-text="'Übung starten'"
		@on-pressed="exerciseStart"
	/>
</template>