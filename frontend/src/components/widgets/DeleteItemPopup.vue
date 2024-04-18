<script setup lang="ts">
	import CloseButton from './CloseButton.vue'

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
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<CloseButton @close="emit('close-popup')" />
			<h2>{{ props.name }}</h2>
			<button id="deleteButton" @click="emit('delete')">
				{{ props.deleteText }}
			</button>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		position: relative;
		background-color: white;
		padding: 20px;
		border-radius: 8px;
	}

	h2 {
		margin: 0px 50px;
	}

	#deleteButton {
		position: relative;
		background-color: #ee4035;
		color: white;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 180px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}
</style>