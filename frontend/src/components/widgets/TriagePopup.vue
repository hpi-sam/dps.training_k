<script setup lang="ts">
	import socketPatient from "@/sockets/SocketPatient"
	import {ref} from 'vue'
	import CloseButton from "./CloseButton.vue"

	const emit = defineEmits(['close-popup'])

	function setTriage(triage: string) {
		socketPatient.triage(triage)
	}

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

	function getTriageColor(color: string) {
		return "var(--"+color+")"
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<h2>Sichtungsfarbe auswählen</h2>
			<div class="button-container">
				<button
					v-for="triageButton in triageButtons"
					:key="triageButton.char"
					class="triage-button"
					:style="{backgroundColor: getTriageColor(triageButton.color)}"
					@click="setTriage(triageButton.char)"
				>
					{{ triageButton.char }}
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
	h2{
		margin: 0px 50px;
	}

	.button-container {
		margin-top: 10px;
		display: flex;
		justify-content: center;
	}

	.triage-button {
		width: 50px;
		height: 50px;
        position: relative;
        border: none;
		padding: 0px;
		margin: 10px;
		margin-right: 5px;
		margin-bottom: 5px;
		align-items: center;
		font-size: 1.25rem;
		color: white;
	}
</style>