<script setup lang="ts">
	import {ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import ButtonMainAction from "@/components/widgets/ButtonMainAction.vue"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {svg} from "@/assets/Svg"
	import {setArea} from "@/components/screensTrainer/ScreenResourceCreation.vue"
	import AreaPopup from '../widgets/AreaPopup.vue'

	const exerciseStore = useExerciseStore()

	function exerciseStart() {
		socketTrainer.exerciseStart()
	}

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

	function addArea(){
		socketTrainer.areaAdd()
	}

	const showPopup = ref(false)
</script>

<template>
	<AreaPopup v-if="showPopup" :area-name="currentArea" @close-popup="showPopup=false" />
	<TopBarTrainer />
	<div class="list">
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
		<button class="listItemAddButton" @click="addArea()">
			Bereich hinzufügen
		</button>
	</div>
	<ButtonMainAction
		:button-text="'Übung starten'"
		@on-pressed="exerciseStart"
	/>
</template>

<style scoped>
	.list {
		margin-top: 90px;
	}

	.settingsButton {
		height: 50px;
		width: 50px;
		border: none;
		background-color: rgb(243, 244, 246);
	}

	.selected .areaButton {
		filter: brightness(90%);
	}
</style>