<script setup lang="ts">
	import {usePatientStore} from '@/stores/Patient'
	import {useResourceAssignmentsStore} from '@/stores/ResourceAssignments'
	import {computed, ref} from 'vue'
	import socketPatient from '@/sockets/SocketPatient'
	import MovePopup from '@/components/widgets/MovePopup.vue'
	import {useExerciseStore} from "@/stores/Exercise"
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemRight} from "@/components/widgets/List"

	const patientStore = usePatientStore()
	const resourceAssignmentStore = useResourceAssignmentsStore()
	const exerciseStore = useExerciseStore()

	const assignments = computed(() => resourceAssignmentStore.getResourceAssignmentsOfArea(patientStore.areaId))

	const assignedPersonnel = computed(() => assignments.value?.personnel.filter(assignment => assignment.patientId === patientStore.patientId))
	const busyPersonnel = computed(() => assignments.value?.personnel.filter(assignment =>
		assignment.patientId != patientStore.patientId &&
		assignment.patientId != null && assignment.patientId != ''
	))
	const freePersonnel = computed(() => assignments.value?.personnel.filter(personnelAssignment => personnelAssignment.patientId === null))

	function releasePersonnel(personnelId: number) {
		socketPatient.releasePersonnel(personnelId)
	}

	function assignPersonnel(personnelId: number) {
		socketPatient.assignPersonnel(personnelId)
	}

	const selectedPersonnel = ref(Number.NEGATIVE_INFINITY)
	const showMovePopup = ref(false)

	function openMovePopup(personnelId: number) {
		selectedPersonnel.value = personnelId
		showMovePopup.value = true
	}
</script>

<template>
	<MovePopup
		v-if="showMovePopup"
		:module="'Patient'"
		:type-to-move="'Personnel'"
		:id-of-moveable="selectedPersonnel" 
		:current-area="patientStore.areaId"
		@close-popup="showMovePopup=false"
	/>
	<div class="flex-container">
		<div class="scroll">
			<h1>Personal</h1>
			<CustomList v-if="assignedPersonnel?.length">
				<p>Diesem Patienten zugeordnet</p>
				<ListItem
					v-for="personnelAssignment in assignedPersonnel"
					:key="personnelAssignment.personnelId"
				>
					<ListItemButton>
						<ListItemName :name="exerciseStore.getPersonnel(personnelAssignment.personnelId)?.personnelName" />
					</ListItemButton>
					<button class="button-free" @click="releasePersonnel(personnelAssignment.personnelId)">
						Freigeben
					</button>
				</ListItem>
			</CustomList>
			<CustomList v-if="freePersonnel?.length">
				<p>Freies Personal</p>
				<ListItem
					v-for="personnelAssignment in freePersonnel"
					:key="personnelAssignment.personnelId"
				>
					<ListItemButton @click="openMovePopup(personnelAssignment.personnelId)">
						<ListItemName :name="exerciseStore.getPersonnel(personnelAssignment.personnelId)?.personnelName" />
					</ListItemButton>
					<button class="button-assign" @click="assignPersonnel(personnelAssignment.personnelId)">
						Zuweisen
					</button>
				</ListItem>
			</CustomList>
			<CustomList v-if="busyPersonnel?.length">
				<p>Anderen Patienten zugeordnet</p>
				<ListItem
					v-for="personnelAssignment in busyPersonnel"
					:key="personnelAssignment.personnelId"
				>
					<ListItemButton>
						<ListItemName :name="exerciseStore.getPersonnel(personnelAssignment.personnelId)?.personnelName" />
						<ListItemRight>
							{{ exerciseStore.getPatient(personnelAssignment.patientId)?.patientName }}
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

	.list-item-right {
		margin-right: 16px;
	}
</style>