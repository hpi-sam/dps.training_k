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
	import {ref} from "vue"

	export const Screens = {
		STATUS: ScreenStatus,
		ACTIONS: ScreenActions,
	} as const
	// eslint-disable-next-line no-redeclare
	type Screens = typeof Screens[keyof typeof Screens]

	const currentLeftScreen = ref(Screens.STATUS)
	const currentRightScreen = ref(Screens.ACTIONS)

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