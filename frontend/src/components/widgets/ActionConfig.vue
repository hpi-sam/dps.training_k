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
				Warte bis wieder neue Aktionen angeordnet werden können.
			</h3>
			<button class="add-action-button" :disabled="!newActionsAllowed" @click="addAction()">
				Aktion anordnen
			</button>
		</div>
	</div>
</template>

<style scoped>
	h1 {
		text-align: center;
		margin-top: 30px;
	}
	.flex-container {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		height: 100%;
		position: relative;
	}
	.close-button {
		display: flex;
		justify-content: center;
		align-items: center;
		position: absolute;
		align-self: flex-end;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		top: 1rem;
		right: 1rem;
		width: 3rem;
		height: 3rem;
		font-size: 1.25rem;
		line-height: 1.25rem;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
	}
	.add-action-button {
		align-self: center;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: calc(100% - 2rem);
		font-size: 1.25rem;
		line-height: 1.25rem;
		padding: .75rem 1rem;
		margin: 1rem;
		text-align: center;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
	}
	.waiting-text {
		text-align: center;
	}
</style>