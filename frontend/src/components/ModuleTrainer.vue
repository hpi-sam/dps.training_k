<template>
	<div id="leftScreen">
		<component :is="screens[currentLeftScreen]" />
	</div>
	<div id="rightScreen">
		<component :is="screens[currentRightScreen]" />
	</div>
</template>

<script setup>
	import {onBeforeUnmount, onMounted} from 'vue';
	import socketTrainer from "@/sockets/SocketTrainer.js";
	import {connectionStore} from "@/sockets/ConnectionStore.js";

	onMounted(() => socketTrainer.connect());
	onBeforeUnmount(() => {
		if (connectionStore.trainerConnected) socketTrainer.close();
	});

	const setLeftScreen = (newScreen) => {
		currentLeftScreen.value = newScreen;
	}

	const setRightScreen = (newScreen) => {
		currentRightScreen.value = newScreen;
	}

	defineExpose({
		setLeftScreen,
		setRightScreen
	});
</script>

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