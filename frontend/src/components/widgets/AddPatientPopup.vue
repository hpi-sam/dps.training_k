<script setup lang="ts">
	import {useAvailablesStore} from "@/stores/Availables"
	import PatientInfo from "./PatientInfo.vue"
	import {computed, ref} from "vue"
	import TriageForListItems from "./TriageForListItems.vue"
	import socketTrainer from "@/sockets/SocketTrainer"
	import PatientCodeList from "./PatientCodeList.vue"
	import {showErrorToast} from "@/App.vue"
	import CloseButton from "./CloseButton.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		areaName: {
			type: String,
			default: 'No Area'
		},
	})

	const firstNameList = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah']
	const surnameList = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis']

	function generateName() {
		const firstName = firstNameList[Math.floor(Math.random() * firstNameList.length)]
		const surname = surnameList[Math.floor(Math.random() * surnameList.length)]
		return `${firstName} ${surname}`
	}


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
			<div id="leftSide">
				<div class="flex-container">
					<h2>Patienten-Datensätze</h2>
					<PatientCodeList @change-patient="changePatientCode" />
				</div>
			</div>
			<div id="rightSide">
				<div class="listItem">
					<TriageForListItems :patient-code="currentPatient?.code" />
					<div class="patientName">
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
	.popup {
		position: relative;
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
		display: flex;
		flex-direction: column;
	}

	#buttonRow {
		display: flex;
	}

	#saveButton {
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