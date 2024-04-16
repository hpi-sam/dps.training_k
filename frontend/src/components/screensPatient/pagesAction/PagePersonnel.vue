<script setup lang="ts">
	import { useExerciseStore } from '@/stores/Exercise'
	import { usePatientStore } from '@/stores/Patient'
	import { useRessourceAssignmentsStore } from '@/stores/RessourceAssignments'
	import {computed} from 'vue'
	import socketPatient from '@/sockets/SocketPatient'

	const patientStore = usePatientStore()
	const ressourceAssignmentStore = useRessourceAssignmentsStore()
	const assignments = computed(() => ressourceAssignmentStore.getRessourceAssignmentsOfArea(patientStore.areaName))
	
	const exerciseStore = useExerciseStore()
	const personnel = computed(() => exerciseStore.getPersonnelOfArea(patientStore.areaName))

	const assignedPersonnel = computed(() => assignments.value?.personnel.filter(assignment => assignment.patientId === patientStore.patientId))
	const freePersonnel = computed(() => personnel.value.filter(personnel => 
		!assignments.value?.personnel.some(assignment => assignment.personnelId === personnel.personnelId)
	))
	const busyPersonnel = computed(() => assignments.value?.personnel.filter(assignment => 
		assignment.patientId != patientStore.patientId && 
		assignment.patientId != null
	))

	function releasePersonnel(personnelId: number) {
		socketPatient.releasePersonnel(personnelId)
	}

	function assignPersonnel(personnelId: number) {
		socketPatient.assignPersonnel(personnelId)
	}
</script>

<template>
	<div class="flex-container">
		<div class="scroll">
			<h1>Personal</h1>
			<div class="list">
				<div v-if="assignedPersonnel?.length">
					<p>Diesem Patienten zugeordnet</p>
					<div
						v-for="personnelAssignment in assignedPersonnel"
						:key="personnelAssignment.personnelId"
						class="listItem"
					>
						<div class="listItemButton">
							<div class="listItemName">
								{{ personnelAssignment.personnelName }}
							</div>
						</div>
						<button class="button-free" @click="releasePersonnel(personnelAssignment.personnelId)">
							Freigeben
						</button>
					</div>
				</div>
				<div v-if="freePersonnel.length">
					<br>
					<p>Freies Personal</p>
					<div
						v-for="personnelAssignment in freePersonnel"
						:key="personnelAssignment.personnelId"
						class="listItem"
					>
						<div class="listItemButton">
							<div class="listItemName">
								{{ personnelAssignment.personnelName }}
							</div>
						</div>
						<button class="button-assign" @click="assignPersonnel(personnelAssignment.personnelId)">
							Zuweisen
						</button>
					</div>
				</div>
				<div v-if="busyPersonnel?.length">
					<br>
					<p>Anderen Patienten zugeordnet</p>
					<div
						v-for="personnelAssignment in busyPersonnel"
						:key="personnelAssignment.personnelId"
						class="listItem"
					>
						<div class="listItemButton">
							<div class="listItemName">
								{{ personnelAssignment.personnelName }}
							</div>
							<div class="listItemName assigned-patient">
								Patient {{ personnelAssignment.patientId }}
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