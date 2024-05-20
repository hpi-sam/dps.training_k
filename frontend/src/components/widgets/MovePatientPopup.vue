<script setup lang="ts">
	import { computed } from "vue"
	import CloseButton from "./CloseButton.vue"
    import { useExerciseStore } from "@/stores/Exercise"
	import socketPatient from "@/sockets/SocketPatient"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		currentArea: {
			type: String,
			default: 'Kein Bereich ausgewählt'
		}
	})

	const exerciseStore = useExerciseStore()

	const areas = computed(() => exerciseStore.getAreaNames.filter(areaName => areaName !== props.currentArea))

	function movePatient(areaName: string) {
		socketPatient.movePatient(areaName)
		emit('close-popup')
	}
</script> 
<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<div class="scroll">
				<h2>Patient verlegen</h2>
				<div class="list">
					<div
						v-for="areaName in areas"
						:key="areaName"
						class="list-item"
					>
						<button class="list-item-button" @click="movePatient(areaName)">
							<div class="list-item-name">
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