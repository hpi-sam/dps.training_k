<script setup lang="ts">
	import CloseButton from './CloseButton.vue'

	const emit = defineEmits(['close-popup','button-click'])

	const props = defineProps({
		title: {
			type: String,
			default: "Unbekannt"
		},
        buttonText: {
            type: String,
            default: "Bestätigen"
        },
        buttonColor: {
            type: String,
            default: ""
        },
        buttonTextColor: {
            type: String,
            default: ""
        }
	})
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup">
			<CloseButton @close="emit('close-popup')" />
			<h2>{{ props.title }}</h2>
			<button
				id="button"
				:style="{backgroundColor: props.buttonColor, color: props.buttonTextColor}"
				@click="emit('button-click')"
			>
				{{ props.buttonText }}
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

	#button {
		position: relative;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 180px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}
</style>