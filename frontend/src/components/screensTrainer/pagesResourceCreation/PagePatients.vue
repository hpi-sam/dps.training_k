<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import EditPatientPopup from '@/components/widgets/EditPatientPopup.vue'
	import AddPatientPopup from '@/components/widgets/AddPatientPopup.vue'
	import TriageForListItems from '@/components/widgets/TriageForListItems.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemLeft, ListItemRight} from "@/components/widgets/List"
	import BinButton from '@/components/widgets/BinButton.vue'
	import socketTrainer from "@/sockets/SocketTrainer"
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'

	const props = defineProps({
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const showDeletePopup = ref(false)
	const showEditPatientPopup = ref(false)
	const showAddPatientPopup = ref(false)

	const currentPatientId = ref('No Patient Id')
	const currentPatientName = computed(() => exerciseStore.getPatient(currentPatientId.value)?.patientName)

	function editPatient(patientId: string) {
		currentPatientId.value = patientId
		showEditPatientPopup.value = true
	}

	function addPatient() {
		showAddPatientPopup.value = true
	}

	function deletePatient() {
		socketTrainer.patientDelete(currentPatientId.value)
	}

	function openDeletePopup(patientId: string) {
		currentPatientId.value = patientId
		showDeletePopup.value = true
	}
</script>

<template>
	<DeleteItemPopup
		v-if="showDeletePopup"
		:name="currentPatientName"
		@close-popup="showDeletePopup=false"
		@delete="deletePatient"
	/>
	<EditPatientPopup v-if="showEditPatientPopup" :patient-id="currentPatientId" @close-popup="showEditPatientPopup=false" />
	<AddPatientPopup v-if="showAddPatientPopup" :area-id="currentArea" @close-popup="showAddPatientPopup=false" />
	<h1>Patienten</h1>
	<CustomList>
		<ListItemAddButton v-if="currentAreaData" id="create-patient-button" text="Patient hinzufügen" @click="addPatient()" />
		<ListItem
			v-for="patient in currentAreaData?.patients"
			:key="patient.patientName"
		>
			<ListItemButton>
				<ListItemLeft @click="editPatient(patient.patientId)">
					{{ patient.patientId }}
				</ListItemLeft>
				<TriageForListItems :patient-code="patient.code" @click="editPatient(patient.patientId)" />
				<ListItemName :name="patient.patientName" @click="editPatient(patient.patientId)" />
				<ListItemRight>
					<BinButton @click="openDeletePopup(patient.patientId)" />
				</ListItemRight>
			</ListItemButton>
		</ListItem>
	</CustomList>
</template>