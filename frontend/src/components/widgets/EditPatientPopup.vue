<script setup lang="ts">
	import {useAvailablesStore} from "@/stores/Availables"
	import PatientInfo from "./PatientInfo.vue"
	import {computed, ref} from "vue"
	import TriageForListItems from "./TriageForListItems.vue"
	import {useExerciseStore} from "@/stores/Exercise"
	import socketTrainer from "@/sockets/SocketTrainer"
	import PatientCodeList from "./PatientCodeList.vue"
	import CloseButton from "./CloseButton.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		patientId: {
			type: String,
			default: ''
		}
	})

	function deletePatient(patientId: string) {
		socketTrainer.patientDelete(patientId)
		emit('close-popup')
	}

	function updatePatient(patientId: string, patientName: string, patientCode: number) {
		socketTrainer.patientUpdate(patientId, patientName, patientCode)
		emit('close-popup')
	}

	const exerciseStore = useExerciseStore()
	const currentPatientName = computed(() => exerciseStore.getPatient(props.patientId)?.patientName)
	const currentPatientCode = ref(exerciseStore.getPatient(props.patientId)?.code)

	const availablesStore = useAvailablesStore()

	const currentPatient = computed(() => {
		if (currentPatientCode.value !== undefined) {
			return availablesStore.getPatient(currentPatientCode.value)
		}
		return null
	})

	function changePatientCode(patientCode: number) {
		currentPatientCode.value = patientCode
	}

</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<div id="leftSide">
				<div class="flex-container">
					<h2>Patienten-Datensätze</h2>
					<PatientCodeList @change-patient="changePatientCode" />
				</div>
			</div>
			<div id="rightSide">
				<div class="flex-container">
					<div class="listItem">
						<div class="patientId">
							{{ props.patientId }}
						</div>
						<TriageForListItems :patient-code="currentPatient?.code" />
						<div class="patientName">
							{{ currentPatientName }}
						</div>
					</div>
					<div class="scroll">
						<PatientInfo
							:injury="currentPatient?.injury"
							:biometrics="currentPatient?.biometrics"
							:consecutive-unique-number="currentPatient?.consecutiveUniqueNumber"
							:mobility="currentPatient?.mobility"
							:preexisting-illnesses="currentPatient?.preexistingIllnesses"
							:permanent-medication="currentPatient?.permanentMedication"
							:current-case-history="currentPatient?.currentCaseHistory"
							:pretreatment="currentPatient?.pretreatment"
						/>
					</div>
					<div id="buttonRow">
						<button id="deleteButton" @click="deletePatient(props.patientId)">
							Löschen
						</button>
						<button
							id="saveButton"
							@click="updatePatient(props.patientId, currentPatientName || '', currentPatient?.code || Number.NEGATIVE_INFINITY)"
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
		margin-left: 10px;
	}

	.listItem {
		margin-right: 40px;
		font-size: 1.25rem;
		text-align: left;
		height: 50px;
		padding-left: 0;
	}

	.patientId, .patientName {
		padding: .75rem 1rem;
	}
</style>