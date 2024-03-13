<script setup lang="ts">
	const props = defineProps({
		injury: {
			type: String,
			default: 'No Injury'
		},
		history: {
			type: String,
			default: 'No Injury'
		},
		personalDetails: {
			type: String,
			default: 'No Injury'
		},
		biometrics: {
			type: String,
			default: 'No Injury'
		}

	})
</script>

<template>
	<p class="key">
		Verletzung
	</p>{{ props.injury }}
	<br>
	<p class="key">
		Vorerkrankungen
	</p>{{ props.history }}
	<br>
	<p class="key">
		Personalien
	</p>{{ props.personalDetails }}
	<br>
	<p class="key">
		Biometrie
	</p>{{ props.biometrics }}
	<br>
</template>

<style scoped>
	.key {
		font-weight: bold;
	}
</style>