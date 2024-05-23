<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {svg} from "@/assets/Svg"
	import {setArea} from "@/components/screensTrainer/ScreenResourceCreation.vue"
	import DeleteItemPopup from '../widgets/DeleteItemPopup.vue'
	import ExerciseControlPanel from '../widgets/ExerciseControlPanel.vue'
	import {Screens, setRightScreen} from '../ModuleTrainer.vue'

	const exerciseStore = useExerciseStore()

	const areas = computed(() => exerciseStore.areas)

	const currentArea = ref(Number.NEGATIVE_INFINITY)

	function openArea(areaId: number) {
		setArea(areaId)
		setRightScreen(Screens.RESOURCE_CREATION)
		currentArea.value = areaId
	}

	function openPopup(areaId: number) {
		openArea(areaId)
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
		currentArea.value = Number.NEGATIVE_INFINITY
	}

	const showPopup = ref(false)
</script>

<template>
	<DeleteItemPopup v-if="showPopup" :name="exerciseStore.getAreaName(currentArea)" @close-popup="showPopup=false" @delete="deleteArea" />
	<div class="flex-container">
		<TopBarTrainer />
		<div class="scroll">
			<div class="list">
				<p v-if="exerciseStore?.status !== 'not-started'">
					<i>Die Bearbeitung der Übung nach Übungsstart ist noch nicht vollständig implementiert.</i>
				</p>
				<br v-if="exerciseStore?.status !== 'not-started'">
				<button id="add-area-button" class="list-item-add-button" @click="addArea()">
					Bereich hinzufügen
				</button>
				<div
					v-for="area in areas"
					:key="area.areaId"
					class="list-item"
					:class="{ 'selected': currentArea === area.areaId }"
				>
					<button class="list-item-button" @click="openArea(area.areaId)">
						<div class="list-item-name">
							{{ area.areaName }}
						</div>
					</button>
					<button class="settings-button" @click="openPopup(area.areaId)">
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
		margin-bottom: 110px;
	}

	.main-button {
		background-color: var(--green);
		color: white;
		margin-bottom: 80px;
	}
</style>