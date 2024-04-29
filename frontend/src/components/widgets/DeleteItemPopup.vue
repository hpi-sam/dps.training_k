<script setup lang="ts">
	import ButtonPopup from './ButtonPopup.vue'

	const emit = defineEmits(['close-popup','delete'])

	const props = defineProps({
		name: {
			type: String,
			default: "Kein Name angegeben"
		},
        deleteText: {
            type: String,
            default: "Löschen"
        }
	})
</script>

<template>
	<ButtonPopup
		:title="props.name"
		:button-text="props.deleteText"
		button-color="var(--red)"
		button-text-color="white"
		@button-click="emit('delete')"
		@close-popup="emit('close-popup')"
	/>
</template>