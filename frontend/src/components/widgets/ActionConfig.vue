<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'
	import { ref } from 'vue'
	import CloseButton from './CloseButton.vue'

	const emit = defineEmits(['close-action'])

	const props = defineProps({
		currentAction: {
			type: String,
			default: "Kein Name angegeben"
		}
	})

	function addAction() {
		socketPatient.actionAdd(props.currentAction)
		newActionsAllowed.value = false
		emit('close-action')
	}

</script>
<script lang="ts">
	const newActionsAllowed = ref(true)

	export function allowNewActions() {
		newActionsAllowed.value = true
	}
</script>

<template>
	<div class="flex-container">
		<div>
			<CloseButton @close="emit('close-action')" />
			<h1>{{ props.currentAction }}</h1>
		</div>
		<div>
			<h3 v-if="!newActionsAllowed" class="waiting-text">
				Warte, bis wieder neue Aktionen angeordnet werden können.
			</h3>
			<button class="main-button" :disabled="!newActionsAllowed" @click="addAction()">
				Aktion anordnen
			</button>
		</div>
	</div>
</template>

<style scoped>
	.waiting-text {
		text-align: center;
	}

	.main-button {
		background-color: var(--green);
		color: white;
	}

	.main-button:disabled {
		background-color: var(--gray);
	}
</style>