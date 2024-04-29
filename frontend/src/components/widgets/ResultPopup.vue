<script setup lang="ts">
	import CloseButton from './CloseButton.vue'

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
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<h2>{{ props.name }}</h2>
			<p>{{ props.result }}</p>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		max-width: 50vw;
	}

	h2 {
		margin: 0px 50px;
	}
</style>