<script setup lang="ts">
	import { useAvailablesStore } from "@/stores/Availables"
	import PatientInfo from "./PatientInfo.vue"
	import { computed, ref } from "vue"
	import TriageForListItems from "./TriageForListItems.vue"
	import { useExerciseStore } from "@/stores/Exercise"
	import socketTrainer from "@/sockets/SocketTrainer"
	import PatientCodeList from "./PatientCodeList.vue"
	import {showErrorToast} from "@/App.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		patientId: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		},
		patientName: {
			type: String,
			default: 'No Name'
		}
	})

	const exerciseStore = useExerciseStore()

	function addPatient(){
		if(!patientCodeChanged) {
			showErrorToast('Es wurde kein Patientencode ausgewählt')
			return
		}
		const areaName = exerciseStore.getAreaOfPatient(props.patientId)?.toString()
		socketTrainer.patientAdd(areaName || '', props.patientId, props.patientName, currentPatientCode.value || Number.NEGATIVE_INFINITY)
	}

	const currentPatientCode = ref(exerciseStore.getPatient(props.patientId)?.patientCode)

	const availablesStore = useAvailablesStore()

	const currentPatient = computed(() => {
		if (currentPatientCode.value !== undefined) {
			return availablesStore.getPatient(currentPatientCode.value)
		}
		return null
	})

	let patientCodeChanged = false
	
	function changePatientCode(patientCode: number){
		currentPatientCode.value = patientCode
		patientCodeChanged = true
	}

</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<div id="leftSide">
				<PatientCodeList @change-patient="changePatientCode" />
			</div>
			<div id="rightSide">
				<div class="listitem">
					<div class="patientId">
						{{ props.patientId }}
					</div>
					<TriageForListItems :patient-code="currentPatient?.patientCode" />
					<div class="patientName">
						{{ props.patientName }}
					</div>
				</div>
				<PatientInfo
					:injury="currentPatient?.patientInjury"
					:history="currentPatient?.patientHistory"
					:biometrics="currentPatient?.patientBiometrics"
					:personal-details="currentPatient?.patientPersonalDetails"
				/>
				<div id="buttonRow">
					<button
						id="saveButton"
						@click="addPatient()"
					>
						Patient hinzufügen
					</button>
				</div>
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
		display: flex;
	}

	#leftSide {
		float: left;
		display: flex;
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
		background-color: #ee4035;
	}

	#saveButton {
		background-color: #269f42;
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
	
	.red {
		background-color: red;
	}

	.yellow {
		background-color: yellow;
	}

	.green {
		background-color: green;
	}
</style>