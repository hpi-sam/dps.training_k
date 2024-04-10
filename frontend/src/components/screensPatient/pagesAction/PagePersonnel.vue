<script setup lang="ts">
	import { usePatientStore } from '@/stores/Patient'
	import { useRessourceAssignmentsStore } from '@/stores/RessourceAssignments'
	import {computed} from 'vue'

	const patientStore = usePatientStore()

	const ressourceAssignmentStore = useRessourceAssignmentsStore()

	const assignments = computed(() => ressourceAssignmentStore.getRessourceAssignmentsOfArea(patientStore.areaName))

	const assignedPersonnel = computed(() => assignments.value?.personnel.filter(assignment => assignment.patientId === patientStore.patientId))

	const freePersonnel = computed(() => assignments.value?.personnel.filter(assignment => assignment.patientId === null))

	const busyPersonnel = computed(() => assignments.value?.personnel.filter(assignment => 
		assignment.patientId != patientStore.patientId && 
		assignment.patientId != null
	))
</script>

<template>
	<h1>Personal</h1>
	<div class="list">
		<p>Diesem Patienten zugeordnet</p>
		<div
			v-for="personnelAssignment in assignedPersonnel"
			:key="personnelAssignment.personnelId"
			class="listItem"
		>
			<button class="listItemButton">
				<div class="listItemName">
					Personal {{ personnelAssignment.personnelId }}
				</div>
			</button>
			<button class="button-free">
				Freigeben
			</button>
		</div>
		<br>
		<p>Freies Personal</p>
		<div
			v-for="personnelAssignment in freePersonnel"
			:key="personnelAssignment.personnelId"
			class="listItem"
		>
			<button class="listItemButton">
				<div class="listItemName">
					Personal {{ personnelAssignment.personnelId }}
				</div>
			</button>
			<button class="button-assign">
				Zuweisen
			</button>
		</div>
		<br>
		<p>Anderen Patienten zugeordnet</p>
		<div
			v-for="personnelAssignment in busyPersonnel"
			:key="personnelAssignment.personnelId"
			class="listItem"
		>
			<button class="listItemButton">
				<div class="listItemName">
					Personal {{ personnelAssignment.personnelId }}
				</div>
				<div class="listItemName assigned-patient">
					Patient {{ personnelAssignment.patientId }}
				</div>
			</button>
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
		background-color: var(--green);
		border: none;
		font-size: 1.25rem;
		width: 120px;
		justify-content: center;
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