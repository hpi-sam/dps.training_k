<script setup lang="ts">
	import {onBeforeUnmount, onMounted} from 'vue'
	import socketPatient from "@/sockets/SocketPatient"
	import {connection} from "@/stores/Connection"

	onMounted(() => socketPatient.connect())
	onBeforeUnmount(() => {
		if (connection.patientConnected) socketPatient.close()
	})
</script>

<script lang="ts">
	import ScreenStatus from './screensPatient/ScreenStatus.vue'
	import ScreenActions from './screensPatient/ScreenActions.vue'
	import {computed, ref} from "vue"

	export enum Screens {
		STATUS = "ScreenStatus",
		ACTIONS = "ScreenActions",
	}

	const currentLeftScreen = ref(Screens.STATUS)
	const currentLeftScreenComponent = computed(() => getScreenComponent(currentLeftScreen.value))
	const currentRightScreen = ref(Screens.ACTIONS)
	const currentRightScreenComponent = computed(() => getScreenComponent(currentRightScreen.value))

	const getScreenComponent = (screen: Screens) => {
		switch (screen) {
			case Screens.STATUS:
				return ScreenStatus
			case Screens.ACTIONS:
				return ScreenActions
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
		position: relative;
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