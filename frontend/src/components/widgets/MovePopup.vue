<script setup lang="ts">
	import {computed} from "vue"
	import CloseButton from "./CloseButton.vue"
    import {useExerciseStore} from "@/stores/Exercise"
	import socketPatient from "@/sockets/SocketPatient"
	import socketTrainer from "@/sockets/SocketTrainer"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		module: {
			type: String,
			default: 'Kein Modul ausgewählt'
		},
		typeToMove: {
			type: String,
			default: 'Kein Typ ausgewählt'
		},
		idOfMoveable: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		},
		currentArea: {
			type: String,
			default: 'Kein Bereich ausgewählt'
		}
	})

	const exerciseStore = useExerciseStore()

	const areas = computed(() => exerciseStore.getAreaNames.filter(areaName => areaName !== props.currentArea))

	function move(areaName: string) {
		if (props.module === 'Patient') {
			if (props.typeToMove === 'Patient') 
				socketPatient.movePatient(areaName)
			else if (props.typeToMove === 'Personnel')
				socketPatient.movePersonnel(props.idOfMoveable, areaName)
			else if (props.typeToMove === 'Material')
				socketPatient.moveMaterial(props.idOfMoveable, areaName)
			else 
				console.error('Invalid type to move')
		} else if (props.module === 'Trainer') {
			if (props.typeToMove === 'Patient') 
				socketTrainer.movePatient(areaName)
			else if (props.typeToMove === 'Personnel')
				socketTrainer.movePersonnel(props.idOfMoveable, areaName)
			else if (props.typeToMove === 'Material')
				socketTrainer.moveMaterial(props.idOfMoveable, areaName)
			else
				console.error('Invalid type to move')
		} else 
			console.error('Invalid module')
		emit('close-popup')
	}

	const title = computed(() => {
		if (props.typeToMove === 'Patient') return 'Patient verlegen'
		if (props.typeToMove === 'Personnel') return 'Personal verlegen'
		if (props.typeToMove === 'Material') return 'Material verlegen'
		return 'Kein Typ ausgewählt'
	})
</script> 
<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<div class="scroll">
				<h2>{{ title }}</h2>
				<div class="list">
					<div
						v-for="areaName in areas"
						:key="areaName"
						class="listItem"
					>
						<button class="listItemButton" @click="move(areaName)">
							<div class="listItemName">
								{{ areaName }}
							</div>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<style scoped>
	.popup {
		position: relative;
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		height: 50vh;
		width: 50vw;
	}
</style>