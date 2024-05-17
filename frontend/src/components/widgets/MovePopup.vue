<script setup lang="ts">
	import { computed, ref } from "vue"
	import CloseButton from "./CloseButton.vue"
    import { useExerciseStore } from "@/stores/Exercise"
	import socketPatient from "@/sockets/SocketPatient"
import socketTrainer from "@/sockets/SocketTrainer";

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
		currentArea: {
			type: String,
			default: 'Kein Bereich ausgewählt'
		}
	})

	const exerciseStore = useExerciseStore()

	const areas = computed(() => exerciseStore.getAreaNames.filter(areaName => areaName !== props.currentArea))

	function move(areaName: string) {
		if ((props.module !== 'Patient' && props.module !== 'Personnel') || 
			(props.typeToMove !== 'Patient' && props.typeToMove !== 'Personnel' && props.typeToMove !== 'Material'))
			console.error('Invalid module or type to move')
		if (props.module === 'Patient') {
			if (props.typeToMove === 'Patient') 
				socketPatient.movePatient(areaName)
			else if (props.typeToMove === 'Personnel')
				socketPatient.movePersonnel(areaName)
			else if (props.typeToMove === 'Material')
				socketPatient.moveMaterial(areaName)
		} else if (props.module === 'Personnel') {
			if (props.typeToMove === 'Patient') 
				socketTrainer.movePatient(areaName)
			else if (props.typeToMove === 'Personnel')
				socketTrainer.movePersonnel(areaName)
			else if (props.typeToMove === 'Material')
				socketTrainer.moveMaterial(areaName)
		}
		emit('close-popup')
	}

	const title = computed(() => {
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