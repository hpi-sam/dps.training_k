<script setup lang="ts">
import { computed } from 'vue'

	const props = defineProps({
		personalDetails: {type: String, default: '-'},
		injury: {type: String, default: '-'},
		biometrics: {type: String, default: '-'},
		mobility: {type: String, default: '-'},
		preexistingIllnesses: {type: String, default: '-'},
		permanentMedication: {type: String, default: '-'},
		currentCaseHistory: {type: String, default: '-'},
		pretreatment: {type: String, default: '-'},
	})

	const infos = computed(() => [
		{name: 'Verletzungen', value: props.injury},
		{name: 'Biometrie', value: props.biometrics},
		{name: 'Mobilität', value: props.mobility},
		{name: 'Vorerkrankungen', value: props.preexistingIllnesses},
		{name: 'Dauer-Medikation', value: props.permanentMedication},
		{name: 'Aktuelle Anamnese / Rettungsdienst-Übergabe', value: props.currentCaseHistory},
		{name: 'Vorbehandlung', value: props.pretreatment},
	])
</script>

<template>
	<table>
		<tr v-for="info in infos" :key="info.name">
			<td colspan="2">
				<br>
				<b>{{ info.name }}</b>
				<br>
				{{ info.value }}
			</td>
		</tr>
	</table>
</template>

<style scoped>
	b {
		font-weight: bold;
	}

	td {
		text-align: left;
	}
</style>