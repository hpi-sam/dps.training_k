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
	import {computed, ref} from "vue"
	import ScreenStatus from "@/components/screensPatient/ScreenStatus.vue"

	export enum Screens {
		CREATE_EXERCISE = "ScreenCreateExercise",
		JOIN_EXERCISE = "ScreenJoinExercise",
		EXERCISE_CREATION = "ScreenExerciseCreation",
		RESOURCE_CREATION = "ScreenResourceCreation"
	}

	const currentLeftScreen = ref(Screens.CREATE_EXERCISE)
	const currentLeftScreenComponent = computed(() => getScreenComponent(currentLeftScreen.value))
	const currentRightScreen = ref(Screens.JOIN_EXERCISE)
	const currentRightScreenComponent = computed(() => getScreenComponent(currentRightScreen.value))

	const getScreenComponent = (screen: Screens) => {
		switch (screen) {
			case Screens.CREATE_EXERCISE:
				return ScreenCreateExercise
			case Screens.JOIN_EXERCISE:
				return ScreenJoinExercise
			case Screens.EXERCISE_CREATION:
				return ScreenExerciseCreation
			case Screens.RESOURCE_CREATION:
				return ScreenResourceCreation
			default:
				return ScreenStatus
		}
	}

	export const setLeftScreen = (newScreen: Screens) => {
		currentLeftScreen.value = newScreen
	}

	export const setRightScreen = (newScreen: Screens) => {
		currentRightScreen.value = newScreen
	}
</script>

<template>
	<div id="leftScreen">
		<component :is="currentLeftScreenComponent" />
	</div>
	<div id="rightScreen">
		<component :is="currentRightScreenComponent" />
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