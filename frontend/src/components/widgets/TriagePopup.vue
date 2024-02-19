<script setup>
	import {usePatientStore} from '@/stores/Patient';

	const emit = defineEmits(['close-popup'])
	const patientStore = usePatientStore()

	
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<h2>Sichtungsfarbe auswählen</h2>
			<div class="button-container">
				<button class="gray" @click="patientStore.triage = '-'">
					-
				</button>
				<button class="green" @click="patientStore.triage = 'G'">
					G
				</button>
				<button class="yellow" @click="patientStore.triage = 'Y'">
					Y
				</button>
				<button class="red" @click="patientStore.triage = 'A'">
					A
				</button>
				<button class="red" @click="patientStore.triage = 'B'">
					B
				</button>
				<button class="red" @click="patientStore.triage = 'C'">
					C
				</button>
				<button class="red" @click="patientStore.triage = 'D'">
					D
				</button>
				<button class="red" @click="patientStore.triage = 'E'">
					E
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.gray{
		background-color: lightgray;
	}

	.green{
		background-color: green;
	}

	.yellow{
		background-color: yellow;
	}

	.red{
		background-color: red;
	}

	.popup-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		text-align: center;
	}

	.popup {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
	}

	.button-container {
		margin-top: 10px;
		display: flex;
		justify-content: center;
	}

	.button-container > button{
		width: 50px;
		height: 50px;
		margin: 10px;
	}
</style>