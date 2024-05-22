<script setup lang="ts">
	import {useAvailablesStore} from "@/stores/Availables"
	import '@/assets/main.css'
	import TriageForListItems from "./TriageForListItems.vue"

	const availablesStore = useAvailablesStore()
	const availablePatients = availablesStore.patients

	const emit = defineEmits(['change-patient'])

	function changePatient(code: number) {
		emit('change-patient', code)
	}
</script>

<template>
	<div class="scroll">
		<div class="list">
			<button
				v-for="patient in availablePatients"
				:key="patient.code"
				class="available-patient-button"
				@click="changePatient(patient.code)"
			>
				<TriageForListItems :patient-code="patient.code" />
			</button>
		</div>
	</div>
</template>

<style scoped>
	.available-patient-button {
		position: relative;
		border: none;
		padding: 0px;
		margin-right: 5px;
		margin-bottom: 5px;
		align-items: center;
		font-size: 1.25rem;
		height: 50px;
	}
</style>
  