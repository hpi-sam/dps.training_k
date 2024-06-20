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
	import ScreenExerciseCreation from './screensTrainer/ScreenExerciseCreation.vue'
	import ScreenResourceCreation from './screensTrainer/ScreenResourceCreation.vue'
	import {computed, ref} from "vue"
	import ScreenStatus from "@/components/screensPatient/ScreenStatus.vue"
	import ScreenLog from "@/components/screensTrainer/ScreenLog.vue"

	export enum Screens {
		EXERCISE_CREATION = "ScreenExerciseCreation",
		RESOURCE_CREATION = "ScreenResourceCreation",
		LOG = "ScreenLog",
	}

	const currentLeftScreen = ref(Screens.EXERCISE_CREATION)
	const currentLeftScreenComponent = computed(() => getScreenComponent(currentLeftScreen.value))
	const currentRightScreen = ref(Screens.RESOURCE_CREATION)
	const currentRightScreenComponent = computed(() => getScreenComponent(currentRightScreen.value))

	const getScreenComponent = (screen: Screens) => {
		switch (screen) {
			case Screens.EXERCISE_CREATION:
				return ScreenExerciseCreation
			case Screens.RESOURCE_CREATION:
				return ScreenResourceCreation
			case Screens.LOG:
				return ScreenLog
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
	<div class="left-screen">
		<component :is="currentLeftScreenComponent" />
	</div>
	<div class="right-screen">
		<component :is="currentRightScreenComponent" />
	</div>
</template>