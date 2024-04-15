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

	const firstNameList =  ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah']
    const surnameList = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis']

	function generateName(){
		const firstName = firstNameList[Math.floor(Math.random() * firstNameList.length)]
		const surname = surnameList[Math.floor(Math.random() * surnameList.length)]
		return `${firstName} ${surname}`
	}

	const newPatientName = ref('No Name')

	function addPatient() {
		newPatientName.value = generateName()
		showAddPatientPopup.value = true
	}
</script>

<template>
	<EditPatientPopup v-if="showEditPatientPopup" :patient-id="currentPatientId" @close-popup="showEditPatientPopup=false" />
	<AddPatientPopup v-if="showAddPatientPopup" :area-name="currentArea" :patient-name="newPatientName" @close-popup="showAddPatientPopup=false" />
	<div class="scroll">
		<h1>Patients</h1>
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
						{{ patient.patientId.toString().padStart(3, '0') }}
					</div>
					<TriageForListItems :patient-code="patient.patientCode" />
					<div class="listItemName">
						{{ patient.patientName }}
					</div>
				</button>
				<ToggleSwitchForListItems default="active" />
			</div>
		</div>
	</div>
</template>