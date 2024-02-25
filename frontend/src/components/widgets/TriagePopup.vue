<script setup lang="ts">
	import {usePatientStore} from '@/stores/Patient';
	import socketPatient from "@/sockets/SocketPatient";
	import { ref } from 'vue';

	const emit = defineEmits(['close-popup'])

	const setTriage = (triage: string) => {
		usePatientStore().triage = triage
		socketPatient.triage(triage)
	};

	const triageButtons = ref([
		{char: '-', color: 'gray'},
		{char: 'G', color: 'green'},
		{char: 'Y', color: 'yellow'},
		{char: 'A', color: 'red'},
		{char: 'B', color: 'red'},
		{char: 'C', color: 'red'},
		{char: 'D', color: 'red'},
		{char: 'E', color: 'red'},
	])

</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<h2>Sichtungsfarbe auswählen</h2>
			<div class="button-container">
				<button
					v-for="triageButton in triageButtons"
					:key="triageButton.char"
					:style="{backgroundColor: triageButton.color}"
					@click="setTriage(triageButton.char)"
				>
					{{ triageButton.char }}
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
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