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

    <button id="ws-test" @click="socket.emit('test-passthrough')">
      send pass-through test
    </button>

    <!-- change the stringified event to test different server-side events -->
    <button id="ws-test" @click="socket.emit('test-event', JSON.stringify(serverEvents.trainerExerciseCreate))">
      send event test
    </button>

    <p id="ws-test">
      Backend-Proxy: {{ connectionState }}
    </p>
  </div>
</template>

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
		useToast().error(message, {
			position: "top-right",
			timeout: 4000,
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
		});
	}

	/**
	 * @param {string} message
	 */
	export function showWarningToast(message) {
		useToast().warning(message, {
			position: "top-right",
			timeout: 4000,
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
		});
	}
</script>

<script setup>
	import {computed} from 'vue'
	import {serverEvents, configureSocket, socket, state} from '@/socket'
	import ModuleLogin from '@/components/ModuleLogin.vue'
	import ModuleTrainer from '@/components/ModuleTrainer.vue'
	import ModulePatient from '@/components/ModulePatient.vue'

	configureSocket()

	const modules = {
		ModuleLogin,
		ModuleTrainer,
		ModulePatient
	}

	const connectionState = computed(() => state.connected ? "connected" : "disconnected")
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