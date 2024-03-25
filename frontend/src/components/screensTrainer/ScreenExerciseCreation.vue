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
	<div id="list">
		<div
			v-for="area in areas"
			:key="area.areaName"
			class="listitem"
			:class="{ 'selected': currentArea === area.areaName }"
		>
			<button class="areaButton" @click="openArea(area.areaName)">
				{{ area.areaName }}
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
		<button id="addAreaButton" @click="addArea()">
			Bereich hinzufügen
		</button>
	</div>
	<ButtonMainAction
		:button-text="'Übung starten'"
		@on-pressed="exerciseStart"
	/>
</template>

<style scoped>
	#list {
		margin-top: 90px;
		margin-left: 30px;
		margin-right: 30px;
	}

	.listitem {
		position: relative;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		display: flex;
		align-items: center;
		text-align: left;
		margin-top: -1px;
	}

	.areaButton {
		position: relative;
		background-color: #FFFFFF;
		border: none;
		display: flex;
		align-items: center;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: left;
		height: 50px;
		width: 100%;
	}

	.settingsButton {
		height: 50px;
		width: 50px;
		border: none;
		background-color: rgb(243, 244, 246);
	}

	#addAreaButton {
		text-align: center;
		position: relative;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		box-sizing: border-box;
		width: 100%;
		font-size: 1.25rem;
		line-height: 1.25rem;
		padding: .75rem 1rem;
		margin-top: -1px;
	}

	.selected .areaButton {
		filter: brightness(90%);
	}
</style>