<script setup lang="ts">
	import {useAvailablesStore} from '@/stores/Availables'
	import {triageToColor} from '@/utils'

	const props = defineProps({
		patientCode: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const availablesStore = useAvailablesStore()

	function getPatientCodeLabel(code: number) {
		if (code === Number.NEGATIVE_INFINITY) {
			return ""
		}
		return code.toString().padStart(4, '0')
	}
</script>

<template>
	<div class="patient-code" :style="{ backgroundColor: triageToColor(availablesStore.getPatient(patientCode)?.triage) }">
		{{ getPatientCodeLabel(props.patientCode) }}
	</div>
</template>

<style scoped>
	.patient-code {
		position: relative;
		display: inline-block;
		height: 50px;
		padding: .75rem 1rem;
		display: flex;
		align-items: center;
		color: white;
	}
</style>