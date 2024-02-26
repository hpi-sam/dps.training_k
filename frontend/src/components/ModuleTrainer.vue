<script setup lang="ts">
	import {onBeforeUnmount, onMounted} from 'vue'
	import socketTrainer from "@/sockets/SocketTrainer"
	import {connection} from "@/stores/Connection"

	onMounted(() => socketTrainer.connect())
	onBeforeUnmount(() => {
		if (connection.trainerConnected) socketTrainer.close()
	})
</script>

<script lang="ts">
	import ScreenCreateExercise from './screensTrainer/ScreenCreateExercise.vue'
	import ScreenJoinExercise from './screensTrainer/ScreenJoinExercise.vue'
	import ScreenExerciseCreation from './screensTrainer/ScreenExerciseCreation.vue'
	import ScreenResourceCreation from './screensTrainer/ScreenResourceCreation.vue'
	import {ref} from "vue"

	export const Screens = {
		CREATE_EXERCISE: ScreenCreateExercise,
		JOIN_EXERCISE: ScreenJoinExercise,
		EXERCISE_CREATION: ScreenExerciseCreation,
		RESOURCE_CREATION: ScreenResourceCreation
	} as const
	// eslint-disable-next-line no-redeclare
	type Screens = typeof Screens[keyof typeof Screens]

	const currentLeftScreen = ref(Screens.CREATE_EXERCISE)
	const currentRightScreen = ref(Screens.JOIN_EXERCISE)

	export const setLeftScreen = (newScreen: Screens) => {
		currentLeftScreen.value = newScreen
	}

	export const setRightScreen = (newScreen: Screens) => {
		currentRightScreen.value = newScreen
	}
</script>

<template>
	<div id="leftScreen">
		<component :is="currentLeftScreen" />
	</div>
	<div id="rightScreen">
		<component :is="currentRightScreen" />
	</div>
</template>

<style scoped>
	#leftScreen, #rightScreen {
		float: left;
		width: 50%;
		height: 100%;
		border: 8px solid black;
	}

	#leftScreen {
		border-right: 4px solid black;
	}

	#rightScreen {
		border-left: 4px solid black;
	}
</style>