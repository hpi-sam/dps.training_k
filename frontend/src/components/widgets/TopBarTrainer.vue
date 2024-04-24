<script setup lang="ts">
	import {useTrainerStore} from "@/stores/Trainer"
	import {useExerciseStore} from "@/stores/Exercise"

	const trainerStore = useTrainerStore()
	const exerciseStore = useExerciseStore()
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
</template>

<style scoped>
	nav {
		width: 100%;
		height: 60px;
		display: flex;
		float: left;
		border-bottom: 2px solid var(--border-color);
	}

	#nav-trainer, #nav-exercise-code {
		width: 50%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.5em;
	}
</style>