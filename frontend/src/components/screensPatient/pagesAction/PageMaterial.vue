<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'
	import {useExerciseStore} from '@/stores/Exercise'
	import {usePatientStore} from '@/stores/Patient'
	import {useResourceAssignmentsStore} from '@/stores/ResourceAssignments'
	import {computed, ref} from 'vue'
	import MovePopup from '@/components/widgets/MovePopup.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemRight} from "@/components/widgets/List"

	const patientStore = usePatientStore()
	const resourceAssignmentStore = useResourceAssignmentsStore()
	const exerciseStore = useExerciseStore()

	const assignments = computed(() => resourceAssignmentStore.getResourceAssignmentsOfArea(patientStore.areaId))

	const assignedMaterial = computed(() => assignments.value?.material.filter(assignment => assignment.patientId === patientStore.patientId))
	const busyMaterial = computed(() => assignments.value?.material.filter(assignment =>
		assignment.patientId != patientStore.patientId &&
		assignment.patientId != null && assignment.patientId != ''
	))
	const freeMaterial = computed(() => assignments.value?.material.filter(personnelAssignment => personnelAssignment.patientId === null))

	function releaseMaterial(materialId: number) {
		socketPatient.releaseMaterial(materialId)
	}

	function assignMaterial(materialId: number) {
		socketPatient.assignMaterial(materialId)
	}

	const selectedMaterial = ref(Number.NEGATIVE_INFINITY)
	const showMovePopup = ref(false)

	function openMovePopup(materialId: number) {
		selectedMaterial.value = materialId
		showMovePopup.value = true
	}
</script>

<template>
	<MovePopup
		v-if="showMovePopup"
		:module="'Patient'"
		:type-to-move="'Material'"
		:id-of-moveable="selectedMaterial" 
		:current-area="patientStore.areaId"
		@close-popup="showMovePopup=false"
	/>
	<div class="flex-container">
		<div class="scroll">
			<h1>Material</h1>
			<CustomList v-if="assignedMaterial?.length">
				<p>Diesem Patienten zugeordnet</p>
				<ListItem
					v-for="materialAssignment in assignedMaterial"
					:key="materialAssignment.materialId"
				>
					<ListItemButton>
						<ListItemName :name="exerciseStore.getMaterial(materialAssignment.materialId)?.materialName" />
					</ListItemButton>
					<button class="button-free" @click="releaseMaterial(materialAssignment.materialId)">
						Freigeben
					</button>
				</ListItem>
			</CustomList>
			<CustomList v-if="freeMaterial?.length">
				<p>Freies Material</p>
				<ListItem
					v-for="materialAssignment in freeMaterial"
					:key="materialAssignment.materialId"
				>
					<ListItemButton @click="openMovePopup(materialAssignment.materialId)">
						<ListItemName :name="exerciseStore.getMaterial(materialAssignment.materialId)?.materialName" />
					</ListItemButton>
					<button class="button-assign" @click="assignMaterial(materialAssignment.materialId)">
						Zuweisen
					</button>
				</ListItem>
			</CustomList>
			<CustomList v-if="busyMaterial?.length">
				<p>Anderen Patienten zugeordnet</p>
				<ListItem
					v-for="materialAssignment in busyMaterial"
					:key="materialAssignment.materialId"
				>
					<ListItemButton>
						<ListItemName :name="exerciseStore.getMaterial(materialAssignment.materialId)?.materialName" />
						<ListItemRight>
							{{ exerciseStore.getPatient(materialAssignment.patientId)?.patientName }}
						</ListItemRight>
					</ListItemButton>
				</ListItem>
			</CustomList>
		</div>
	</div>
</template>

<style scoped>
	.list-item-button {
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