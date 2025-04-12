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
	import ScreenPatientEditor from "@/components/screensTrainer/ScreenPatientEditor.vue"

	export enum ScreenPosition {
		LEFT = "left",
		RIGHT = "right",
		FULL = "full",
	}

	export enum Screens {
		EXERCISE_CREATION = "ScreenExerciseCreation",
		RESOURCE_CREATION = "ScreenResourceCreation",
		LOG = "ScreenLog",
		PATIENT_EDITOR = "ScreenPatientEditor"
	}

	const currentLeftScreen = ref(Screens.EXERCISE_CREATION)
	const currentLeftScreenComponent = computed(() => getScreenComponent(currentLeftScreen.value))
	const currentRightScreen = ref(Screens.RESOURCE_CREATION)
	const currentRightScreenComponent = computed(() => getScreenComponent(currentRightScreen.value))
	const currentFullScreen = ref(Screens.PATIENT_EDITOR)
	const currentFullScreenComponent = computed(() => getScreenComponent(currentFullScreen.value))
	const fullScreen = ref(false)

	const getScreenComponent = (screen: Screens) => {
		switch (screen) {
			case Screens.EXERCISE_CREATION:
				return ScreenExerciseCreation
			case Screens.RESOURCE_CREATION:
				return ScreenResourceCreation
			case Screens.LOG:
				return ScreenLog
			case Screens.PATIENT_EDITOR:
				return ScreenPatientEditor
			default:
				return ScreenStatus
		}
	}

	export const setScreen = (newScreen: Screens, position: String) => {
		switch (position) {
			case 'left':
				currentLeftScreen.value = newScreen
				fullScreen.value = false
				break
			case 'right':
				currentRightScreen.value = newScreen
				fullScreen.value = false
				break
			case 'full':
				currentFullScreen.value = newScreen
				fullScreen.value = true
				break
		}
	}
</script>

<template>
	<div v-if="!fullScreen" class="left-screen">
		<component :is="currentLeftScreenComponent" />
	</div>
	<div v-if="!fullScreen" class="right-screen">
		<component :is="currentRightScreenComponent" />
	</div>
	<div v-if="fullScreen" class="full-screen">
		<component :is="currentFullScreenComponent" />
	</div>
</template>