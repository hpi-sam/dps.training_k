<script setup lang="ts">
	import {ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {svg} from "@/assets/Svg"
	import {setArea} from "@/components/screensTrainer/ScreenResourceCreation.vue"
	import DeleteItemPopup from '../widgets/DeleteItemPopup.vue'
	import ExerciseControlPanel from '../widgets/ExerciseControlPanel.vue'

	const exerciseStore = useExerciseStore()

	const areas = ref(exerciseStore.areas)

	const currentArea = ref("Kein Bereich ausgewählt")

	function openArea(areaName: string) {
		setArea(areaName)
		currentArea.value = areaName
	}

	function openPopup(areaName: string) {
		openArea(areaName)
		showPopup.value = true
	}

	function addArea() {
		socketTrainer.areaAdd()
	}

	function deleteArea() {
		socketTrainer.areaDelete(currentArea.value)
	}

	const showPopup = ref(false)
</script>

<template>
	<DeleteItemPopup v-if="showPopup" :name="currentArea" @close-popup="showPopup=false" @delete="deleteArea" />
	<div class="flex-container">
		<TopBarTrainer />
		<div class="scroll">
			<div class="list">
				<button class="listItemAddButton" @click="addArea()">
					Bereich hinzufügen
				</button>
				<div
					v-for="area in areas"
					:key="area.areaName"
					class="listItem"
					:class="{ 'selected': currentArea === area.areaName }"
				>
					<button class="listItemButton" @click="openArea(area.areaName)">
						<div class="listItemName">
							{{ area.areaName }}
						</div>
					</button>
					<button class="settingsButton" @click="openPopup(area.areaName)">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							height="24"
							viewBox="0 -960 960 960"
							width="24"
						>
							<path :d="svg.settingsIcon" />
						</svg>
					</button>
				</div>
			</div>
		</div>
		<ExerciseControlPanel />
	</div>
</template>

<style scoped>
	.settingsButton {
		height: 50px;
		width: 50px;
		border: none;
		background-color: rgb(243, 244, 246);
		margin-left: auto;
	}

	@-moz-document url-prefix() { /* for Firefox */
		.scroll {
			margin-bottom: 50px;
		}
	}

	.main-button {
		background-color: var(--green);
		color: white;
	}
</style>