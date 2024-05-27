<script setup lang="ts">
	import {usePatientStore} from '@/stores/Patient'
	import {useResourceAssignmentsStore} from '@/stores/ResourceAssignments'
	import {computed, ref} from 'vue'
	import socketPatient from '@/sockets/SocketPatient'
	import MovePopup from '@/components/widgets/MovePopup.vue'
	import {useExerciseStore} from "@/stores/Exercise"

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
			<div class="list">
				<div v-if="assignedPersonnel?.length">
					<p>Diesem Patienten zugeordnet</p>
					<div
						v-for="personnelAssignment in assignedPersonnel"
						:key="personnelAssignment.personnelId"
						class="list-item"
					>
						<button class="list-item-button">
							<div class="list-item-name">
								{{ exerciseStore.getPersonnel(personnelAssignment.personnelId)?.personnelName }}
							</div>
						</button>
						<button class="button-free" @click="releasePersonnel(personnelAssignment.personnelId)">
							Freigeben
						</button>
					</div>
				</div>
				<div v-if="freePersonnel?.length">
					<br>
					<p>Freies Personal</p>
					<div
						v-for="personnelAssignment in freePersonnel"
						:key="personnelAssignment.personnelId"
						class="list-item"
					>
						<button class="list-item-button" @click="openMovePopup(personnelAssignment.personnelId)">
							<div class="list-item-name">
								{{ exerciseStore.getPersonnel(personnelAssignment.personnelId)?.personnelName }}
							</div>
						</button>
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
						class="list-item"
					>
						<button class="list-item-button">
							<div class="list-item-name">
								{{ exerciseStore.getPersonnel(personnelAssignment.personnelId)?.personnelName }}
							</div>
							<div class="list-item-name assigned-patient">
								{{ exerciseStore.getPatient(personnelAssignment.patientId)?.patientName }}
								({{ personnelAssignment.patientId }})
							</div>
						</button>
					</div>
				</div>
			</div>
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