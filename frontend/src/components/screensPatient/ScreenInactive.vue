<script setup lang="ts">
	import {usePatientStore} from "@/stores/Patient"
	import {useExerciseStore} from "@/stores/Exercise"

	const patientStore = usePatientStore()
	const exerciseStore = useExerciseStore()
</script>

<template>
	<div class="inactive-patient-container">
		<div class="content">
			<div class="inactive-patient-header">
				Patient inaktiv
			</div>
			<div class="inactive-patient-details">
				<p>
					Patient: {{ patientStore.patientName }} | {{ patientStore.patientId }}
				</p>
				<p v-if="exerciseStore.getAreaName(patientStore.areaId)">
					Bereich: {{ exerciseStore.getAreaName(patientStore.areaId) }}
				</p>
				<p v-if="patientStore.inactiveInfo">
					{{ patientStore.inactiveInfo }}
				</p>
				<p v-if="patientStore.timeUntilBack > 0">
					{{ new Date(new Date(0).setSeconds(patientStore.timeUntilBack)).toISOString().substring(14, 19) }}
				</p>
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
