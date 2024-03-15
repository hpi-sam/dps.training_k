<script setup lang="ts">
	import { useAvailablesStore } from '@/stores/Availables'

    const props = defineProps({
		patientCode: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const availablesStore = useAvailablesStore()

	function getTriageColor(patientCode: number) {
		if(availablesStore.getPatient(patientCode)?.triage){
			return availablesStore.getPatient(patientCode)?.triage
		}
		return "gray"
	}

	function getPatientCodeLabel(patientCode: number) {
		if (patientCode === Number.NEGATIVE_INFINITY) {
			return ""
		}
		return patientCode.toString()
	}
</script>

<template>
	<div :class="getTriageColor(props.patientCode)" class="patientCode">
		{{ getPatientCodeLabel(props.patientCode) }}
	</div>
</template>

<style scoped>
	.patientCode {
		position: relative;
		display: inline-block;
		height: 50px;
		padding: .75rem 1rem;
		display: flex;
		align-items: center;
		text-align: center;
	}
</style>