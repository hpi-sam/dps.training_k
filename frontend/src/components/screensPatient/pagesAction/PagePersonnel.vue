<script setup lang="ts">
	import { usePatientStore } from '@/stores/Patient'
	import { useRessourceAssignmentsStore } from '@/stores/RessourceAssignments'
	import {computed} from 'vue'

	const patientStore = usePatientStore()

	const ressourceAssignmentStore = useRessourceAssignmentsStore()

	const assignments = computed(() => ressourceAssignmentStore.getRessourceAssignmentsOfArea(patientStore.areaName))
</script>

<template>
	<h1>Personal</h1>
	<div class="list">
		<div
			v-for="personnelAssignment in assignments?.personnel"
			:key="personnelAssignment.personnelId"
			class="listItem"
		>
			<button class="listItemButton">
				<div class="listItemName">
					Personal {{ personnelAssignment.personnelId }} ist Patient {{ personnelAssignment.patientId }} zugeordnet
				</div>
			</button>
		</div>
	</div>
</template>