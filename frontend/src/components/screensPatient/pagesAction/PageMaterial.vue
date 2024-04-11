<script setup lang="ts">
	import { useExerciseStore } from '@/stores/Exercise'
	import { usePatientStore } from '@/stores/Patient'
	import { useRessourceAssignmentsStore } from '@/stores/RessourceAssignments'
	import {computed} from 'vue'

	const patientStore = usePatientStore()
	const ressourceAssignmentStore = useRessourceAssignmentsStore()
	const assignments = computed(() => ressourceAssignmentStore.getRessourceAssignmentsOfArea(patientStore.areaName))

	const exerciseStore = useExerciseStore()
	const material = computed(() => exerciseStore.getMaterialOfArea(patientStore.areaName))

	const assignedMaterial = computed(() => assignments.value?.material.filter(assignment => assignment.patientId === patientStore.patientId))
	const freeMaterial = computed(() => material.value.filter(material => 
		!assignments.value?.material.some(assignment => assignment.materialId === material.materialId)
	))
	const busyMaterial = computed(() => assignments.value?.material.filter(assignment => 
		assignment.patientId != patientStore.patientId && 
		assignment.patientId != null
	))
</script>

<template>
	<h1>Material</h1>
	<div class="list">
		<p>Diesem Patienten zugeordnet</p>
		<div
			v-for="materialAssignment in assignedMaterial"
			:key="materialAssignment.materialId"
			class="listItem"
		>
			<div class="listItemButton">
				<div class="listItemName">
					{{ materialAssignment.materialName }}
				</div>
			</div>
			<button class="button-free">
				Freigeben
			</button>
		</div>
		<br>
		<p>Freies Material</p>
		<div
			v-for="materialAssignment in freeMaterial"
			:key="materialAssignment.materialId"
			class="listItem"
		>
			<div class="listItemButton">
				<div class="listItemName">
					{{ materialAssignment.materialName }}
				</div>
			</div>
			<button class="button-assign">
				Zuweisen
			</button>
		</div>
		<br>
		<p>Anderen Patienten zugeordnet</p>
		<div
			v-for="materialAssignment in busyMaterial"
			:key="materialAssignment.materialId"
			class="listItem"
		>
			<div class="listItemButton">
				<div class="listItemName">
					{{ materialAssignment.materialName }}
				</div>
				<div class="listItemName assigned-patient">
					Patient {{ materialAssignment.patientId }}
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.listItemButton {
		padding-right: 0;
	}

	.button-assign, .button-free {
		position: relative;
		display: inline-block;
		height: 50px;
		padding: .75rem 1rem;
		display: flex;
		align-items: center;
		color: white;
		border: none;
		font-size: 1.25rem;
		width: 120px;
		justify-content: center;
	}

	.button-free {
		background-color: var(--red);
	}

	.button-assign {
		background-color: var(--green);
	}

	.assigned-patient {
		margin-left: auto;
		position: relative;
		display: inline-block;
		height: 50px;
		padding: .75rem 1rem;
		display: flex;
		align-items: center;
		border: none;
		font-size: 1.25rem;
		justify-content: center;
	}
</style>