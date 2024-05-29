<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import EditPatientPopup from '@/components/widgets/EditPatientPopup.vue'
	import AddPatientPopup from '@/components/widgets/AddPatientPopup.vue'
	import TriageForListItems from '@/components/widgets/TriageForListItems.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemLeft} from "@/components/widgets/List"

	const props = defineProps({
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const showEditPatientPopup = ref(false)
	const showAddPatientPopup = ref(false)

	const currentPatientId = ref('')

	function editPatient(patientId: string) {
		currentPatientId.value = patientId
		showEditPatientPopup.value = true
	}

	function addPatient() {
		showAddPatientPopup.value = true
	}
</script>

<template>
	<EditPatientPopup v-if="showEditPatientPopup" :patient-id="currentPatientId" @close-popup="showEditPatientPopup=false" />
	<AddPatientPopup v-if="showAddPatientPopup" :area-id="currentArea" @close-popup="showAddPatientPopup=false" />
	<h1>Patienten</h1>
	<CustomList>
		<ListItemAddButton v-if="currentAreaData" id="create-patient-button" text="Patient hinzufügen" @click="addPatient()" />
		<ListItem
			v-for="patient in currentAreaData?.patients"
			:key="patient.patientName"
		>
			<ListItemButton @click="editPatient(patient.patientId)">
				<ListItemLeft>
					{{ patient.patientId }}
				</ListItemLeft>
				<TriageForListItems :patient-code="patient.code" />
				<ListItemName :name="patient.patientName" />
			</ListItemButton>
		</ListItem>
	</CustomList>
</template>