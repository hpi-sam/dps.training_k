<script setup lang="ts">
	import {ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import ButtonMainAction from "@/components/widgets/ButtonMainAction.vue"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {svg} from "@/assets/Svg"
	import {setArea} from "@/components/screensTrainer/ScreenResourceCreation.vue"

	const exerciseStore = useExerciseStore()

	function exerciseStart() {
		socketTrainer.exerciseStart()
	}

	const areas = ref(exerciseStore.areas)

	const openArea = (areaName: string) => {
		setArea(areaName)
	}
</script>

<template>
	<TopBarTrainer />
	<div id="list">
		<button
			v-for="area in areas"
			:key="area.areaName"
			class="areaButtons"
			@click="openArea(area.areaName)"
		>
			{{ area.areaName }}
			<svg
				id="settingsIcon"
				xmlns="http://www.w3.org/2000/svg"
				height="24"
				viewBox="0 -960 960 960"
				width="24"
			>
				<path :d="svg.settingsIcon" />
			</svg>
		</button>
		<button id="addAreaButton">
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

	.areaButtons {
		position: relative;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		box-sizing: border-box;
		display: flex;
		align-items: center;
		width: 100%;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: left;
		margin-top: -1px;
	}

	#settingsIcon {
		margin-left: auto;
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
</style>