<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'
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
	const freeMaterial = computed(() => material.value?.filter(material => 
		!assignments.value?.material.some(assignment => assignment.materialId === material.materialId)
	))
	const busyMaterial = computed(() => assignments.value?.material.filter(assignment => 
		assignment.patientId != patientStore.patientId && 
		assignment.patientId != null
	))

	function releaseMaterial(materialId: number) {
		socketPatient.releaseMaterial(materialId)
	}

	function assignMaterial(materialId: number) {
		socketPatient.assignMaterial(materialId)
	}
</script>

<template>
	<div class="flex-container">
		<div class="scroll">
			<h1>Material</h1>
			<div class="list">
				<div v-if="assignedMaterial?.length">
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
						<button class="button-free" @click="releaseMaterial(materialAssignment.materialId)">
							Freigeben
						</button>
					</div>
				</div>
				<div v-if="freeMaterial?.length">
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
						<button class="button-assign" @click="assignMaterial(materialAssignment.materialId)">
							Zuweisen
						</button>
					</div>
				</div>
				<div v-if="busyMaterial?.length">
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