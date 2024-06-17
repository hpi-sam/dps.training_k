<script setup lang="ts">
	import {computed} from 'vue'
	import socketPatient, {serverMockEvents as serverMockEventsPatient} from "@/sockets/SocketPatient"
	import socketTrainer, {serverMockEvents as serverMockEventsTrainer} from "@/sockets/SocketTrainer"
	import {connection} from "@/stores/Connection"

	const runMode = import.meta.env.VITE_RUN_CONFIG

	const connectionState = computed(() => {
		if (currentModule.value === Modules.TRAINER) return connection.trainerConnected
		else if (currentModule.value === Modules.PATIENT) return connection.patientConnected
		else return false
	})

	const serverMockEvents = computed(() => {
		if (currentModule.value === Modules.TRAINER) return serverMockEventsTrainer
		else if (currentModule.value === Modules.PATIENT) return serverMockEventsPatient
		else return serverMockEventsPatient
	})

	const selectedMockEvent = ref(serverMockEvents.value[0].id)

	const mockEvent = () => {
		const event = serverMockEvents.value.find(e => e.id === selectedMockEvent.value)
		if (!event) return
		const messageEvent = {data: event.data} as MessageEvent

		if (currentModule.value === Modules.TRAINER && socketTrainer.socket?.onmessage) {
			socketTrainer.socket.onmessage(messageEvent)
		} else if (socketPatient.socket?.onmessage) {
			socketPatient.socket.onmessage(messageEvent)
		} else {
			showErrorToast('Event mocking failed: no socket available')
			return
		}

		showWarningToast(`Mocked Server Event: ${event.id}`)
	}

	const sendPasstroughTest = () => {
		if (currentModule.value === Modules.TRAINER)
			socketTrainer.testPassthrough()
		else if (currentModule.value === Modules.PATIENT)
			socketPatient.testPassthrough()
	}
</script>

<script lang="ts">
	import {POSITION, TYPE, useToast} from "vue-toastification"
	import {ref} from "vue"
	import type {ToastOptions} from "vue-toastification/dist/types/types"
	import ModuleLogin from "@/components/ModuleLogin.vue"
	import ModuleTrainer from "@/components/ModuleTrainer.vue"
	import ModulePatient from "@/components/ModulePatient.vue"

	export enum Modules {
		LOGIN = "ModuleLogin",
		TRAINER = "ModuleTrainer",
		PATIENT = "ModulePatient",
	}

	const currentModule = ref(Modules.LOGIN)

	const currentModuleComponent = computed(() => {
		switch (currentModule.value) {
			case Modules.TRAINER:
				return ModuleTrainer
			case Modules.PATIENT:
				return ModulePatient
			case Modules.LOGIN:
			default:
				return ModuleLogin
		}
	})

	export function setModule(newModule: Modules) {
		currentModule.value = newModule
	}

	export function showErrorToast(message: string) {
		useToast().error(message, getToastOptions())
	}

	export function showWarningToast(message: string) {
		useToast().warning(message, getToastOptions())
	}

	function getToastOptions(): ToastOptions & { type?: TYPE.ERROR & TYPE.WARNING } {
		return {
			position: POSITION.TOP_RIGHT,
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
		New Frontend container
		<component :is="currentModuleComponent" />
	</main>

	<div v-if="runMode == 'dev'" id="dev-bar">
		<button id="login-module-button" @click="currentModule=Modules.LOGIN">
			Login
		</button>
		<button id="trainer-module-button" @click="currentModule=Modules.TRAINER">
			Trainer
		</button>
		<button id="patient-module-button" @click="currentModule=Modules.PATIENT">
			Patient
		</button>

		<button v-if="connectionState" id="ps-test" @click="sendPasstroughTest()">
			send pass-through test
		</button>

		<button v-if="currentModule!==Modules.LOGIN" id="ws-test" @click="mockEvent()">
			Mock Server Event:
		</button>
		<select v-if="currentModule!==Modules.LOGIN" v-model="selectedMockEvent">
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
		background-color: var(--border-color);
		padding: 5px;
	}

	#ws-test, #ps-test {
		margin-left: 20px;
	}
</style>