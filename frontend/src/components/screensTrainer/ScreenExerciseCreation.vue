<script setup lang="ts">
	import {useTrainerStore} from '@/stores/Trainer'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import ButtonMainAction from "@/components/widgets/ButtonMainAction.vue"

	const trainerStore = useTrainerStore()
	const exerciseStore = useExerciseStore()

	function exerciseStart() {
		socketTrainer.exerciseStart()
	}
</script>

<template>
	<nav>
		<div id="nav-trainer">
			{{ trainerStore.username }}
		</div>
		<div id="nav-exercise-code">
			{{ exerciseStore.exerciseId }}
		</div>
	</nav>
	<div>Geladenes Übungsobjekt: <br>{{ exerciseStore }}</div>
	<ButtonMainAction
		:button-text="'Übung starten'"
		@on-pressed="exerciseStart"
	/>
</template>

<style scoped>
	nav {
		width: 100%;
		height: 60px;
		display: flex;
		float: left;
	}

	#nav-trainer, #nav-exercise-code {
		width: 50%;
		height: 100%;
		border-bottom: 8px solid black;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.5em;
	}

	#nav-trainer {
		border-right: 4px solid black;
	}

	#nav-exercise-code {
		border-left: 4px solid black;
	}
</style>