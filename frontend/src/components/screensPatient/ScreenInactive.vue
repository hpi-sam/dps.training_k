<script setup lang="ts">
	import {usePatientStore} from "@/stores/Patient"

	const patientStore = usePatientStore()
</script>

<template>
	<div class="inactive-patient-container">
		<div class="content">
			<div class="inactive-patient-header">
				Patient inaktiv
			</div>
			<div class="inactive-patient-details">
				<div>Patient: {{ patientStore.patientName }} | {{ patientStore.patientID }}</div>
				<div>Bereich: {{ patientStore.areaName }}</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.inactive-patient-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
	}

	.content {
		width: 60%;
		text-align: center;
	}

	.inactive-patient-header {
		font-weight: bold;
		margin-bottom: 8px;
		font-size: 1.5em;
	}

	.inactive-patient-details {
		margin-bottom: 16px;
		font-size: 1.25em;
	}
</style>
