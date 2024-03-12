<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"
	import { useAvailablesStore } from "@/stores/Availables"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		patientId: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const availablePatients = useAvailablesStore().patients
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<div id="leftSide">
				<h2>{{ props.patientId }}</h2>
				<div id="list">
					Hier sollte die Liste stehen
					{{ availablePatients }}
					<div
						v-for="patient in availablePatients"
						:key="patient.patientCode"
						class="listitem"
					>
						<button class="areaButton">
							{{ patient.patientCode }}
						</button>
					</div>
				</div>
			</div>
			<div id="rightSide">
				<button id="deleteButton">
					Löschen
				</button>
				<button id="saveButton">
					Speichern
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.popup-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;
		z-index: 1;
	}

	.popup {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		width: 80vw;
		
	}

	#leftSide, #rightSide {
		float: left;
		display: flex;
		width: 50%;
		padding: 10px;
	}

	#deleteButton, #saveButton {
		position: relative;
		background-color: #ee4035;
		color: white;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 100%;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
		float: left;
	}

	#saveButton {
		background-color: #269f42;
	}

	#list {
		margin-top: 90px;
		margin-left: 30px;
		margin-right: 30px;
	}

	.listitem {
		position: relative;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		display: flex;
		align-items: center;
		text-align: left;
		margin-top: -1px;
	}
</style>