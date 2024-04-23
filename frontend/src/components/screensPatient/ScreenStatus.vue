<script setup lang="ts">
	import {ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient'
	import TriagePopup from '@/components/widgets/TriagePopup.vue'
	import PatientStatus from '@/components/widgets/PatientStatus.vue'
	import { triageToColor } from '@/utils'
	import PatientModel from '../widgets/PatientModel.vue'

	const patientStore = usePatientStore()

	const showPopup = ref(false)
</script>

<template>
	<div class="flex-container">
		<nav>
			<button id="nav-trainer">
				{{ patientStore.patientId }}
			</button>
			<button
				id="nav-triage"
				:style="{backgroundColor: triageToColor(patientStore.triage)}"
				@click="showPopup = true"
			>
				{{ patientStore.triage }}
			</button>
			<button id="nav-exercise-code">
				{{ patientStore.areaName }}
			</button>
		</nav>
		<div class="scroll">
			<div class="overview">
				<PatientModel />
			</div>
			<TriagePopup v-if="showPopup" @close-popup="showPopup=false" />
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

	#nav-exercise-code {
		width: 40%;
	}

	.overview {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>