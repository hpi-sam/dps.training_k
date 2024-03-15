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

	const newPatientId = ref(Number.NEGATIVE_INFINITY)
	const newPatientName = ref('No Name')

	function addPatient() {
		newPatientId.value = exerciseStore.getNewPatientId()
		newPatientName.value = generateName()
		currentPatientId.value = newPatientId.value
		showAddPatientPopup.value = true
	}
</script>

<template>
	<EditPatientPopup v-if="showEditPatientPopup" :patient-id="currentPatientId" @close-popup="showEditPatientPopup=false" />
	<AddPatientPopup v-if="showAddPatientPopup" :patient-id="newPatientId" :patient-name="newPatientName" @close-popup="showAddPatientPopup=false" />
	<div id="list">
		<div
			v-for="patient in currentAreaData?.patients"
			:key="patient.patientName"
			class="listitem"
		>
			<button class="areaButton" @click="editPatient(patient.patientId)">
				<div class="patientId">
					{{ patient.patientId }}
				</div>
				<TriageForListItems :patient-code="patient.patientCode" />
				<div class="patientName">
					{{ patient.patientName }}
				</div>
			</button>
			<ToggleSwitchForListItems default="active" />
		</div>
		<button id="addAreaButton" @click="addPatient()">
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

	.patientId, .patientName {
		padding: .75rem 1rem;
	}
</style>