<script setup lang="ts">
	const emit = defineEmits(['close-popup','delete'])

	const props = defineProps({
		name: {
			type: String,
			default: "Kein Name angegeben"
		},
        result: {
            type: String,
            default: "Kein Ergebnis angegeben"
        }
	})
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<h2>{{ props.name }}</h2>
			<p>{{ props.result }}</p>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		max-width: 50vw;
	}
</style>