<script setup lang="ts">
	import {svg} from '@/assets/Svg'
	import socketPatient from '@/sockets/SocketPatient'
	import { ref } from 'vue'

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
			<h1>{{ props.currentAction }}</h1>
			<button class="close-button" @click="emit('close-action')">
				<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
					<path :d="svg.closeIcon" />
				</svg>
			</button>
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