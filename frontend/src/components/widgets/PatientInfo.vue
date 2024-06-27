<script setup lang="ts">
	import {computed} from 'vue'
	import {strings} from "@/strings"

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
		{name: strings.patientInfo.injury, value: props.injury},
		{name: strings.patientInfo.biometrics, value: props.biometrics},
		{name: strings.patientInfo.mobility, value: props.mobility},
		{name: strings.patientInfo.preexistingIllnesses, value: props.preexistingIllnesses},
		{name: strings.patientInfo.permanentMedication, value: props.permanentMedication},
		{name: strings.patientInfo.currentCaseHistory, value: props.currentCaseHistory},
		{name: strings.patientInfo.pretreatment, value: props.pretreatment},
	])
</script>

<template>
	<table>
		<tr v-for="info in infos" :key="info.name">
			<td colspan="2">
				<br>
				<b>{{ info.name }}</b>
				<br>{{ info.value }}
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