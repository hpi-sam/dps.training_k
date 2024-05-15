<script setup lang="ts">
	import {ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient'
	import TriagePopup from '@/components/widgets/TriagePopup.vue'
	import MovePatientPopup from '@/components/widgets/MovePatientPopup.vue'
	import PatientStatus from '@/components/widgets/PatientStatus.vue'
	import { triageToColor } from '@/utils'
	import PatientModel from '../widgets/PatientModel.vue'

	const patientStore = usePatientStore()

	const showTriagePopup = ref(false)

	const showMovePatientPopup = ref(false)
</script>

<template>
	<TriagePopup v-if="showTriagePopup" @close-popup="showTriagePopup=false" />
	<MovePatientPopup v-if="showMovePatientPopup" :current-area="patientStore.areaName" @close-popup="showMovePatientPopup=false" />
	<div class="flex-container">
		<nav>
			<button id="nav-trainer">
				{{ patientStore.patientName }}
			</button>
			<button
				id="nav-triage"
				:style="{backgroundColor: triageToColor(patientStore.triage)}"
				@click="showTriagePopup = true"
			>
				{{ patientStore.triage }}
			</button>
			<button
				id="nav-area-name"
				@click="showMovePatientPopup = true"
			>
				{{ patientStore.areaName }}
			</button>
		</nav>
		<div class="scroll">
			<div class="overview">
				<PatientModel />
			</div>
			<PatientStatus />
		</div>
	</div>
</template>

<style scoped>
	nav {
		width: 100%;
		height: 60px;
		display: flex;
		float: left;
		border-bottom: 2px solid var(--border-color);
	}

	button {
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.5em;
		background-color: white;
		border: none;
	}

	#nav-trainer {
		width: 40%;
	}

	#nav-triage {
		width: 20%;
		color: white;
	}

	#nav-area-name {
		width: 40%;
	}

	.overview {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		margin-top: 30px;
	}
</style>