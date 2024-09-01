<script setup lang="ts">
	import {computed} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import {usePatientStore} from '@/stores/Patient'

	const exerciseStore = useExerciseStore()
	const patientStore = usePatientStore()

	const title = computed(() => {
		switch (exerciseStore.status) {
			case ExerciseStatus.RUNNING:
				return patientStore.relocatingInfo
			case ExerciseStatus.NOT_STARTED:
				return 'Warte, bis die Übung beginnt'
			case ExerciseStatus.PAUSED:
				return 'Übung pausiert'
			case ExerciseStatus.ENDED:
				return 'Übung beendet'
			default:
				return 'Warte auf Übung'
		}
	})

	const info = computed(() => {
		if (exerciseStore.status == ExerciseStatus.RUNNING) {
			return new Date(new Date(0).setSeconds(patientStore.timeUntilBack)).toISOString().substring(12, 19)
		} else return 'Bereich: '+ exerciseStore.getAreaName(patientStore.areaId)
	})
</script>

<template>
	<div class="container">
		<div class="content">
			<h1>
				{{ title }}
			</h1>
			<h2>
				Patient: {{ patientStore.patientName }} ({{ patientStore.patientId }})
			</h2>
			<h2>
				{{ info }}
			</h2>
		</div>
	</div>
</template>

<style scoped>
	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
	}

	.content {
		width: 60%;
		text-align: center;
	}
</style>
