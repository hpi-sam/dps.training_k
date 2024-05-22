<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {svg} from "@/assets/Svg"
	import {setArea} from "@/components/screensTrainer/ScreenResourceCreation.vue"
	import DeleteItemPopup from '../widgets/DeleteItemPopup.vue'
	import ExerciseControlPanel from '../widgets/ExerciseControlPanel.vue'
	import { Screens, setRightScreen } from '../ModuleTrainer.vue'

	const exerciseStore = useExerciseStore()

	const areas = computed(() => exerciseStore.areas)

	const currentArea = ref("Kein Bereich ausgewählt")

	function openArea(areaName: string) {
		setArea(areaName)
		setRightScreen(Screens.RESOURCE_CREATION)
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

	function openLog() {
		setRightScreen(Screens.LOG)
	}

	const showPopup = ref(false)
</script>

<template>
	<DeleteItemPopup v-if="showPopup" :name="currentArea" @close-popup="showPopup=false" @delete="deleteArea" />
	<div class="flex-container">
		<TopBarTrainer />
		<div class="scroll">
			<div class="list">
				<button id="add-area-button" class="list-item-add-button" @click="addArea()">
					Bereich hinzufügen
				</button>
				<div
					v-for="area in areas"
					:key="area.areaName"
					class="list-item"
					:class="{ 'selected': currentArea === area.areaName }"
				>
					<button class="list-item-button" @click="openArea(area.areaName)">
						<div class="list-item-name">
							{{ area.areaName }}
						</div>
					</button>
					<button class="settings-button" @click="openPopup(area.areaName)">
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
		<div>
			<button v-if="exerciseStore?.status !== 'not-started'" class="main-button" @click="openLog()">
				Log öffnen
			</button>
		</div>
		<ExerciseControlPanel />
	</div>
</template>

<style scoped>
	.settings-button {
		height: 50px;
		width: 50px;
		border: none;
		background-color: rgb(243, 244, 246);
		margin-left: auto;
	}

	.scroll {
		margin-bottom: 50px;
	}

	.main-button {
		background-color: var(--green);
		color: white;
		margin-bottom: 80px;
	}
</style>