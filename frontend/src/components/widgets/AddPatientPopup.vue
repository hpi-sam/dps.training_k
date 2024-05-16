<script setup lang="ts">
	import {useAvailablesStore} from "@/stores/Availables"
	import PatientInfo from "./PatientInfo.vue"
	import {computed, ref} from "vue"
	import TriageForListItems from "./TriageForListItems.vue"
	import socketTrainer from "@/sockets/SocketTrainer"
	import PatientCodeList from "./PatientCodeList.vue"
	import {showErrorToast} from "@/App.vue"
	import CloseButton from "./CloseButton.vue"
	import { generateName } from "@/utils"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		areaName: {
			type: String,
			default: 'No Area'
		},
	})

	const patientName = ref("")
	patientName.value = generateName()

	function addPatient() {
		if (!patientCodeChanged) {
			showErrorToast('Es wurde kein Patientencode ausgewählt')
			return
		}
		socketTrainer.patientAdd(props.areaName, patientName.value, currentPatientCode.value)
		patientName.value = generateName()
	}

	const currentPatientCode = ref()

	const availablesStore = useAvailablesStore()

	const currentPatient = computed(() => {
		if (currentPatientCode.value !== undefined) {
			return availablesStore.getPatient(currentPatientCode.value)
		}
		return null
	})

	let patientCodeChanged = false

	function changePatientCode(patientCode: number) {
		currentPatientCode.value = patientCode
		patientCodeChanged = true
	}

</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<div id="left-side">
				<div class="flex-container">
					<h2>Patienten-Datensätze</h2>
					<PatientCodeList @change-patient="changePatientCode" />
				</div>
			</div>
			<div id="right-side">
				<div class="list-item">
					<TriageForListItems :patient-code="currentPatient?.code" />
					<div class="patient-name">
						{{ patientName }}
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
				<div id="button-row">
					<button
						id="save-button"
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
	.popup {
		position: relative;
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		width: 80vw;
		height: 50vh;
		display: flex;
	}

	#left-side {
		float: left;
		width: 50%;
		padding: 10px;
	}

	#right-side {
		width: 50%;
		padding: 10px;
		display: flex;
		flex-direction: column;
	}

	#button-row {
		display: flex;
	}

	#save-button {
		position: relative;
		color: white;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 100%;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
		background-color: var(--green);
	}

	.list-item {
		margin-right: 40px;
		font-size: 1.25rem;
		text-align: left;
		height: 50px;
		padding-left: 0;
	}

	.patient-id, .patient-name {
		padding: .75rem 1rem;
	}
</style>