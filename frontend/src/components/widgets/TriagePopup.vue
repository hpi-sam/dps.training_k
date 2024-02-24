<script setup>
	import {usePatientStore} from '@/stores/Patient';
	import socketPatient from "@/sockets/SocketPatient";

	const emit = defineEmits(['close-popup'])

	const setTriage = (triage) => {
		usePatientStore().triage = triage
		socketPatient.triage(triage)
	};

</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<h2>Sichtungsfarbe auswählen</h2>
			<div class="button-container">
				<button class="gray" @click="setTriage('-')">
					-
				</button>
				<button class="green" @click="setTriage('G')">
					G
				</button>
				<button class="yellow" @click="setTriage('Y')">
					Y
				</button>
				<button class="red" @click="setTriage('A')">
					A
				</button>
				<button class="red" @click="setTriage('B')">
					B
				</button>
				<button class="red" @click="setTriage('C')">
					C
				</button>
				<button class="red" @click="setTriage('D')">
					D
				</button>
				<button class="red" @click="setTriage('E')">
					E
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.gray {
		background-color: lightgray;
	}

	.green {
		background-color: green;
	}

	.yellow {
		background-color: yellow;
	}

	.red {
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

	.button-container > button {
		width: 50px;
		height: 50px;
		margin: 10px;
	}
</style>