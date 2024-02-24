<script setup>
	import {computed} from 'vue'
	import ModuleLogin from '@/components/ModuleLogin.vue'
	import ModuleTrainer from '@/components/ModuleTrainer.vue'
	import ModulePatient from '@/components/ModulePatient.vue'
	import socketPatient, {serverMockEvents as serverMockEventsPatient} from "@/sockets/SocketPatient";
	import socketTrainer, {serverMockEvents as serverMockEventsTrainer} from "@/sockets/SocketTrainer";
	import {connection} from "@/stores/Connection.js";

	const modules = {
		ModuleLogin,
		ModuleTrainer,
		ModulePatient
	}

	const connectionState = computed(() => {
		if (currentModule.value === 'ModuleTrainer') return connection.trainerConnected
		else if (currentModule.value === 'ModulePatient') return connection.patientConnected
		else return false
	})

	const serverMockEvents = computed(() => {
		if (currentModule.value === 'ModuleTrainer') return serverMockEventsTrainer
		else if (currentModule.value === 'ModulePatient') return serverMockEventsPatient
		else return serverMockEventsPatient
	})

	const selectedMockEvent = ref(serverMockEvents.value[0].id);

	const mockEvent = () => {
		const event = serverMockEvents.value.find(e => e.id === selectedMockEvent.value)
		if (!event) return
		const messageEvent = {data: event.data}

		if (currentModule.value === 'ModuleTrainer')
			socketTrainer.socket.onmessage(messageEvent)
		else socketPatient.socket.onmessage(messageEvent)

		showWarningToast(`Mocked Server Event: ${event.id}`)
	}

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

		<button v-if="connectionState" id="ws-test" @click="sendPasstroughTest()">
			send pass-through test
		</button>

		<button v-if="currentModule!=='ModuleLogin'" id="ws-test" @click="mockEvent()">
			Mock Server Event:
		</button>
		<select v-if="currentModule!=='ModuleLogin'" v-model="selectedMockEvent">
			<option v-for="event in serverMockEvents" :key="event.id" :value="event.id">
				{{ event.id }}
			</option>
		</select>
	</div>
</template>

<style scoped>
	#dev-bar {
		display: flex;
		align-items: center;
	}

	#ws-test {
		margin-left: 20px;
	}
</style>