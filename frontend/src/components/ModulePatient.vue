<script setup>
	import {onBeforeUnmount, onMounted} from 'vue'
	import socketPatient from "@/sockets/SocketPatient.js";
	import {connectionStore} from "@/sockets/ConnectionStore.js";

	onMounted(() => socketPatient.connect());
	onBeforeUnmount(() => {
		if (connectionStore.patientConnected) socketPatient.close();
	});
</script>

<script>
	import ScreenStatus from './screensPatient/ScreenStatus.vue'
	import ScreenActions from './screensPatient/ScreenActions.vue'
	import {ref} from "vue";

	const screens = {
		ScreenStatus,
		ScreenActions
	}

	const currentLeftScreen = ref('ScreenStatus');
	const currentRightScreen = ref('ScreenActions');

	export const setLeftScreen = (newScreen) => {
		currentLeftScreen.value = newScreen;
	}

	export const setRightScreen = (newScreen) => {
		currentRightScreen.value = newScreen;
	}
</script>

<template>
	<div id="leftScreen">
		<component :is="screens[currentLeftScreen]" />
	</div>
	<div id="rightScreen">
		<component :is="screens[currentRightScreen]" />
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