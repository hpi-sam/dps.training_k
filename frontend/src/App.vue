<template>
	<main>
		<component :is="modules[currentModule]" />
	</main>

	<div id="dev-bar">
		<button @click="currentModule='ModuleLogin'">
			Login
		</button>
		<button @click="currentModule='ModuleTrainer'">
			Trainer
		</button>
		<button @click="currentModule='ModulePatient'">
			Patient
		</button>

		<button id="ws-test" @click="sendPasstroughTest()">
			send pass-through test
		</button>

		<!-- change the stringified event to test different server-side events -->
		<!--<button id="ws-test" @click="socket.emit('test-event', JSON.stringify(serverEvents.trainerExerciseCreate))">
			send event test
		</button>-->

		<p id="ws-test">
			Backend state: {{ connectionState }}
		</p>
	</div>
</template>

<script setup>
	import {computed} from 'vue'
	import ModuleLogin from '@/components/ModuleLogin.vue'
	import ModuleTrainer from '@/components/ModuleTrainer.vue'
	import ModulePatient from '@/components/ModulePatient.vue'
	import socketPatient from "@/sockets/SocketPatient.js";
	import socketTrainer from "@/sockets/SocketTrainer.js";
	import {connectionStore} from "@/sockets/ConnectionStore.js";

	const modules = {
		ModuleLogin,
		ModuleTrainer,
		ModulePatient
	}

	const connectionState = computed(() => {
		if (currentModule.value === 'ModuleTrainer')
			return connectionStore.trainerConnected ? "connected" : "disconnected"
		else if (currentModule.value === 'ModulePatient')
			return connectionStore.patientConnected ? "connected" : "disconnected"
		else
			return "n/a"
	})

	const sendPasstroughTest = () => {
		if (currentModule.value === 'ModuleTrainer')
			socketTrainer.testPassthrough();
		else if (currentModule.value === 'ModulePatient')
			socketPatient.testPassthrough();
	};
</script>

<script>
	import {useToast} from "vue-toastification";
	import {ref} from "vue";

	const currentModule = ref('ModuleLogin')

	export function setModule(newModule) {
		currentModule.value = newModule
	}

	/**
	 * @param {string} message
	 */
	export function showErrorToast(message) {
		useToast().error(message, getToastOptions());
	}

	/**
	 * @param {string} message
	 */
	export function showWarningToast(message) {
		useToast().warning(message, getToastOptions());
	}

	/**
	 * @return {ToastOptions}
	 */
	function getToastOptions() {
		return {
			position: "top-right",
			timeout: 5000,
			closeOnClick: true,
			pauseOnFocusLoss: true,
			pauseOnHover: true,
			draggable: true,
			draggablePercent: 0.6,
			showCloseButtonOnHover: false,
			hideProgressBar: true,
			closeButton: "button",
			icon: true,
			rtl: false
		}
	}
</script>

<style scoped>
	#dev-bar {
		display: flex;
		align-items: center;
	}

	#ws-test {
		margin-left: 20px;
	}
</style>