<script setup lang="ts">
	import {usePatientStore} from "@/stores/Patient"
	import socketPatient, {serverMockEvents as serverMockEventsPatient} from "@/sockets/SocketPatient"

	const patientStore = usePatientStore()

	function startExercise() {
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'exercise-started').data} as MessageEvent)
	}

	async function startDemo() {
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'exercise').data} as MessageEvent)
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'available-actions').data} as MessageEvent)
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'exercise-started').data} as MessageEvent)
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'state').data} as MessageEvent)
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'ressource-assignments').data} as MessageEvent)
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'action-list').data} as MessageEvent)
		await new Promise(f => setTimeout(f, 100)) // bc visible-injuries is a bitch <3
		socketPatient.socket.onmessage({data: serverMockEventsPatient.find(e => e.id === 'visible-injuries').data} as MessageEvent)
	}
</script>

<template>
	<div class="inactive-patient-container">
		<div class="content">
			<div class="inactive-patient-header">
				Patient inaktiv
			</div>
			<div class="inactive-patient-details">
				<div>Patient: {{ patientStore.patientName }} | {{ patientStore.patientId }}</div>
				<div>Bereich: {{ patientStore.areaName }}</div>
			</div>



			<button
				id="button"
				:style="{backgroundColor: 'var(--green)', color: 'white', marginRight: '10px'}"
				@click="startExercise"
			>
				Übung starten
			</button>
			<button
				id="button"
				:style="{backgroundColor: 'var(--yellow)', color: 'white'}"
				@click="startDemo"
			>
				Demo starten
			</button>
		</div>
	</div>
</template>

<style scoped>
	.inactive-patient-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
	}

	.content {
		width: 60%;
		text-align: center;
	}

	.inactive-patient-header {
		font-weight: bold;
		margin-bottom: 8px;
		font-size: 1.5em;
	}

	.inactive-patient-details {
		margin-bottom: 16px;
		font-size: 1.25em;
	}

	#button {
		position: relative;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 180px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}
</style>
