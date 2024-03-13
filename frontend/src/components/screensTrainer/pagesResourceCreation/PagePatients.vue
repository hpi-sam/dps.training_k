<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'
	import PatientPopup from '@/components/widgets/PatientPopup.vue'
	import { useAvailablesStore } from '@/stores/Availables'

    const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const showPopup = ref(false)

	const currentPatientId = ref(Number.NEGATIVE_INFINITY)

	function openPatient(patientId: number) {
		currentPatientId.value = patientId
		showPopup.value = true
	}

	const availablesStore = useAvailablesStore()

	function getTriageColor(patientCode: number) {
		return availablesStore.getPatient(patientCode)?.triage
	}
</script>

<template>
	<PatientPopup v-if="showPopup" :patient-id="currentPatientId" @close-popup="showPopup=false" />
	<div id="list">
		<div
			v-for="patient in currentAreaData?.patients"
			:key="patient.patientName"
			class="listitem"
		>
			<button class="areaButton" @click="openPatient(patient.patientId); getTriageColor(patient.patientCode)">
				<div :class="getTriageColor(patient.patientCode)" class="patientCode">
					{{ patient.patientCode }}
				</div>
				<div class="patientName">
					{{ patient.patientName }}
					{{ patient.patientId }}
				</div>
			</button>
			<ToggleSwitchForListItems />
		</div>
		<button id="addAreaButton">
			Patient hinzufügen
		</button>
	</div>
</template>

<style scoped>
	#list {
		margin-top: 30px;
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

	.areaButton {
		position: relative;
		background-color: #FFFFFF;
		border: none;
		display: flex;
		align-items: center;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		padding-left: 0;
		text-align: left;
		height: 50px;
		width: 100%;
	}

	.settingsButton {
		height: 50px;
		width: 50px;
		border: none;
		background-color: rgb(243, 244, 246);
	}

	#addAreaButton {
		text-align: center;
		position: relative;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		box-sizing: border-box;
		width: 100%;
		font-size: 1.25rem;
		line-height: 1.25rem;
		padding: .75rem 1rem;
		margin-top: -1px;
	}

	.patientCode {
		position: relative;
		display: inline-block;
		height: 50px;
		padding: .75rem 1rem;
		display: flex;
		align-items: center;
		text-align: center;
	}

	.patientName {
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