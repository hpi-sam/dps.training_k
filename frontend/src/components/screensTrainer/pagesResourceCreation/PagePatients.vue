<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'

    const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))
</script>

<template>
	<div id="list">
		<div
			v-for="patient in currentAreaData?.patients"
			:key="patient.patientName"
			class="listitem"
		>
			<button class="areaButton">
				{{ patient.patientCode }}
				{{ patient.patientName }}
				{{ patient.patientId }}
			</button>
			<ToggleSwitchForListItems />
		</div>
		<button id="addAreaButton">
			Patient hinzufügen
		</button>
	</div>
</template>

<style scoped>
	#list {
		margin-top: 30px;
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
</style>