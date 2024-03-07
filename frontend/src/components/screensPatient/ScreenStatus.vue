<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient'
	import TriagePopup from '@/components/widgets/TriagePopup.vue'
	import PatientStatus from '@/components/widgets/PatientStatus.vue'

	const patientStore = usePatientStore()

	const triageColor = ref(computed(() => {
		switch (patientStore.triage) {
			case 'G':
				return 'green'
			case 'Y':
				return 'yellow'
			case 'A':
			case 'B':
			case 'C':
			case 'D':
			case 'E':
				return 'red'
			default:
				return 'gray'
		}
	}))

	const showPopup = ref(false)
</script>

<template>
	<nav>
		<button id="nav-trainer">
			{{ patientStore.patientID }}
		</button>
		<button id="nav-triage" :class="triageColor" @click="showPopup = true">
			{{ patientStore.triage }}
		</button>
		<button id="nav-exercise-code">
			{{ patientStore.areaName }}
		</button>
	</nav>
	<TriagePopup v-if="showPopup" @close-popup="showPopup=false" />
	<PatientStatus />
</template>

<style scoped>
	nav {
		width: 100%;
		height: 60px;
		display: flex;
		float: left;
	}

	button {
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.5em;
		background-color: white;
		border: none;
		border-bottom: 8px solid black;
	}

	#nav-trainer {
		width: 40%;
		border-right: 4px solid black;
	}

	#nav-triage {
		width: 20%;
		border-left: 4px solid black;
		border-right: 4px solid black;
	}

	#nav-exercise-code {
		width: 40%;
		border-left: 4px solid black;
	}

	/*noinspection CssUnusedSymbol*/
	.gray {
		background-color: lightgray;
	}

	/*noinspection CssUnusedSymbol*/
	.green {
		background-color: green;
	}

	/*noinspection CssUnusedSymbol*/
	.yellow {
		background-color: yellow;
	}

	/*noinspection CssUnusedSymbol*/
	.red {
		background-color: red;
	}
</style>