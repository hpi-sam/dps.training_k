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
	import ScreenInactive from "@/components/screensPatient/ScreenInactive.vue"

	export enum ScreenPosition {
		LEFT = "left",
		RIGHT = "right",
		FULL = "full",
	}

	export enum Screens {
		STATUS = "ScreenStatus",
		ACTIONS = "ScreenActions",
		INACTIVE = "ScreenInactive",
	}

	const currentLeftScreen = ref(Screens.STATUS)
	const currentLeftScreenComponent = computed(() => getScreenComponent(currentLeftScreen.value))
	const currentRightScreen = ref(Screens.ACTIONS)
	const currentRightScreenComponent = computed(() => getScreenComponent(currentRightScreen.value))
	const currentFullScreen = ref(Screens.INACTIVE)
	const currentFullScreenComponent = computed(() => getScreenComponent(currentFullScreen.value))
	const fullScreen = ref(true)

	const getScreenComponent = (screen: Screens) => {
		switch (screen) {
			case Screens.STATUS:
				return ScreenStatus
			case Screens.ACTIONS:
				return ScreenActions
			case Screens.INACTIVE:
				return ScreenInactive
		}
	}

	export const setScreen = (newScreen: Screens, pos: ScreenPosition) => {
		switch (pos) {
			case ScreenPosition.LEFT:
				currentLeftScreen.value = newScreen
				fullScreen.value = false
				break
			case ScreenPosition.RIGHT:
				currentRightScreen.value = newScreen
				fullScreen.value = false
				break
			case ScreenPosition.FULL:
				currentFullScreen.value = newScreen
				fullScreen.value = true
				break
		}
	}
</script>

<template>
	<div v-if="!fullScreen" id="leftScreen">
		<component :is="currentLeftScreenComponent" />
	</div>
	<div v-if="!fullScreen" id="rightScreen">
		<component :is="currentRightScreenComponent" />
	</div>
	<div v-if="fullScreen" id="fullScreen">
		<component :is="currentFullScreenComponent" />
	</div>
</template>

<style scoped>
	#fullScreen {
		position: relative;
		float: left;
		width: 100%;
		height: 100%;
		border: 8px solid black;
	}

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