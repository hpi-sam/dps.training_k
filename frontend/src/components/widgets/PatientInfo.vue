<script setup lang="ts">
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
</script>

<template>
	<p class="key">
		Verletzungen
	</p>{{ props.injury }}
	<br>
	<p class="key">
		Biometrie
	</p>{{ props.biometrics }}
	<br>
	<p class="key">
		Vorerkrankungen
	</p>{{ props.preexistingIllnesses }}
	<br>
	<p class="key">
		Dauer-Medikation
	</p>{{ props.permanentMedication }}
	<br>
	<p class="key">
		Aktuelle Anamnese / Rettungsdienst-Übergabe
	</p>{{ props.currentCaseHistory }}
	<br>
	<p class="key">
		Vorbehandlung
	</p>{{ props.pretreatment }}
	<br>
	<p class="key">
		Mobilität
	</p>{{ props.mobility }}
</template>

<style scoped>
	.key {
		font-weight: bold;
	}
</style>