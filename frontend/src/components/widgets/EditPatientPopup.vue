<script setup lang="ts">
	import { useAvailablesStore } from "@/stores/Availables"
	import PatientInfo from "./PatientInfo.vue"
	import { computed, ref } from "vue"
	import TriageForListItems from "./TriageForListItems.vue"
	import { useExerciseStore } from "@/stores/Exercise"
	import socketTrainer from "@/sockets/SocketTrainer"
	import PatientCodeList from "./PatientCodeList.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		patientId: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	function deletePatient(patientId: number){
		socketTrainer.patientDelete(patientId)
	}

	function updatePatient(patientId: number, patientName: string, patientCode: number){
		socketTrainer.patientUpdate(patientId, patientName, patientCode)
	}

	const exerciseStore = useExerciseStore()
	const currentPatientName = computed(() => exerciseStore.getPatient(props.patientId)?.patientName)
	const currentPatientCode = ref(exerciseStore.getPatient(props.patientId)?.patientCode)

	const availablesStore = useAvailablesStore()

	const currentPatient = computed(() => {
		if (currentPatientCode.value !== undefined) {
			return availablesStore.getPatient(currentPatientCode.value)
		}
		return null
	})
	
	function changePatientCode(patientCode: number){
		currentPatientCode.value = patientCode
	}

</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<div id="leftSide">
				<div class="flex-container">
					<h2>Patienten-Datensätze</h2>
					<PatientCodeList @change-patient="changePatientCode" />
				</div>
			</div>
			<div id="rightSide">
				<div class="flex-container">
					<div class="listitem">
						<div class="patientId">
							{{ props.patientId.toString().padStart(3, '0') }}
						</div>
						<TriageForListItems :patient-code="currentPatient?.patientCode" />
						<div class="patientName">
							{{ currentPatientName }}
						</div>
					</div>
					<div class="scroll">
						<PatientInfo
							:injury="currentPatient?.patientInjury"
							:history="currentPatient?.patientHistory"
							:biometrics="currentPatient?.patientBiometrics"
							:personal-details="currentPatient?.patientPersonalDetails"
						/>
					</div>
					<div id="buttonRow">
						<button id="deleteButton" @click="deletePatient(props.patientId)">
							Löschen
						</button>
						<button
							id="saveButton"
							@click="updatePatient(props.patientId, currentPatientName || '', currentPatient?.patientCode || Number.NEGATIVE_INFINITY)"
						>
							Speichern
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		width: 80vw;
		height: 50vh;
		display: flex;
	}

	#leftSide {
		float: left;
		width: 50%;
		padding: 10px;
	}

	#rightSide {
		width: 50%;
		padding: 10px;
	}

	#buttonRow {
		display: flex;
	}

	#deleteButton, #saveButton {
		position: relative;
		color: white;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 100%;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}

	#deleteButton {
		background-color: var(--red);
	}

	#saveButton {
		background-color: var(--green);
	}

	.listitem {
		position: relative;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		display: flex;
		align-items: center;
		margin-top: -1px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: left;
		height: 50px;
		width: 100%;
	}

	.listitem {
		padding-left: 0;
	}

	.patientId, .patientName {
		padding: .75rem 1rem;
	}
</style>