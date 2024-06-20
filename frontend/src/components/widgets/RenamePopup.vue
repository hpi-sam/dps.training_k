<script setup lang="ts">
	import {ref} from 'vue'
	import CloseButton from './CloseButton.vue'

	const emit = defineEmits(['close-popup','rename'])

	const props = defineProps({
		name: {
			type: String,
			default: ""
		},
		title: {
			type: String,
			default: "Umbenennen"
		},
        renameText: {
            type: String,
            default: "Umbenennen"
        }
	})

	const name = ref(props.name)

	function renameItem() {
		emit('rename', name.value)
		emit('close-popup')
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<h2>{{ props.title }}</h2>
			<input v-model="name" :placeholder="props.name">
			<br>
			<button
				id="button"
				@click="renameItem()"
			>
				{{ props.renameText }}
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
		background-color: var(--green);
		color: white;
	}

	input{
		border: 1px solid var(--gray);
		border-radius: 10px;
		padding: 5px;
		margin-bottom: 10px;
		margin-top: 20px;
		font-size: 1.5em;
	}
</style>