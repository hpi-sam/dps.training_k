<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'
	import EditPatientPopup from '@/components/widgets/EditPatientPopup.vue'
	import AddPatientPopup from '@/components/widgets/AddPatientPopup.vue'
	import TriageForListItems from '@/components/widgets/TriageForListItems.vue'

	const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const showEditPatientPopup = ref(false)
	const showAddPatientPopup = ref(false)

	const currentPatientId = ref(Number.NEGATIVE_INFINITY)

	function editPatient(patientId: number) {
		currentPatientId.value = patientId
		showEditPatientPopup.value = true
	}

	function addPatient() {
		showAddPatientPopup.value = true
	}
</script>

<template>
	<EditPatientPopup v-if="showEditPatientPopup" :patient-id="currentPatientId" @close-popup="showEditPatientPopup=false" />
	<AddPatientPopup v-if="showAddPatientPopup" :area-name="currentArea" @close-popup="showAddPatientPopup=false" />
	<div class="scroll">
		<h1>Patienten</h1>
		<div class="list">
			<button v-if="currentAreaData" class="listItemAddButton" @click="addPatient()">
				Patient hinzufügen
			</button>
			<div
				v-for="patient in currentAreaData?.patients"
				:key="patient.patientName"
				class="listItem"
			>
				<button class="listItemButton" @click="editPatient(patient.patientId)">
					<div class="listItemId">
						{{ patient.patientId.toString().padStart(6, '0') }}
					</div>
					<TriageForListItems :patient-code="patient.code" />
					<div class="listItemName">
						{{ patient.patientName }}
					</div>
				</button>
				<ToggleSwitchForListItems default="active" />
			</div>
		</div>
	</div>
</template>