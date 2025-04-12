<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from "@/sockets/SocketTrainer"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {setArea} from "@/components/screensTrainer/ScreenResourceCreation.vue"
	import DeleteItemPopup from '../widgets/DeleteItemPopup.vue'
	import ExerciseControlPanel from '../widgets/ExerciseControlPanel.vue'
	import {Screens, setScreen} from '../ModuleTrainer.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemRight} from "@/components/widgets/List"
	import IconButton from '@/components/widgets/IconButton.vue'
	import {svg} from "@/assets/Svg"
	import RenamePopup from '../widgets/RenamePopup.vue'

	const exerciseStore = useExerciseStore()

	const areas = computed(() => exerciseStore.areas)

	const currentArea = ref(Number.NEGATIVE_INFINITY)

	function openArea(areaId: number) {
		setArea(areaId)
		setScreen(Screens.RESOURCE_CREATION, 'right')
		currentArea.value = areaId
	}

	function openDeletePopup() {
		showDeletePopup.value = true
	}

	function openRenamePopup() {
		showRenamePopup.value = true
	}

	function addArea() {
		socketTrainer.areaAdd()
	}

	function deleteArea() {
		socketTrainer.areaDelete(currentArea.value)
	}

	function renameArea(name: string) {
		socketTrainer.areaRename(currentArea.value, name)
	}

	function openLog() {
		setScreen(Screens.LOG, 'right')
		currentArea.value = Number.NEGATIVE_INFINITY
	}

	const showDeletePopup = ref(false)
	const showRenamePopup = ref(false)
</script>

<template>
	<RenamePopup
		v-if="showRenamePopup"
		:name="exerciseStore.getAreaName(currentArea) || ''"
		:title="'Bereich umbenennen'"
		@close-popup="showRenamePopup=false"
		@rename="(name) => renameArea(name)"
	/>
	<DeleteItemPopup
		v-if="showDeletePopup"
		:name="exerciseStore.getAreaName(currentArea) || ''"
		@close-popup="showDeletePopup=false"
		@delete="deleteArea"
	/>
	<div class="flex-container">
		<TopBarTrainer />
		<div class="scroll">
			<CustomList>
				<p v-if="exerciseStore?.status !== 'not-started'">
					<i>Die Bearbeitung der Übung nach Übungsstart ist noch nicht vollständig implementiert.</i>
				</p>
				<br v-if="exerciseStore?.status !== 'not-started'">
				<ListItemAddButton id="add-area-button" text="Bereich hinzufügen" @click="addArea()" />
				<ListItem
					v-for="area in areas"
					:key="area.areaId"
					:class="{ 'selected': currentArea === area.areaId }"
				>
					<ListItemButton>
						<ListItemName :name="area.areaName" @click="openArea(area.areaId)" />
						<ListItemRight>
							<IconButton :icon="svg.penIcon" @click="openArea(area.areaId); openRenamePopup()" />
							<IconButton :icon="svg.binIcon" @click="openArea(area.areaId); openDeletePopup()" />
						</ListItemRight>
					</ListItemButton>
				</ListItem>
			</CustomList>
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
	.scroll {
		margin-bottom: 110px;
	}

	.main-button {
		background-color: var(--green);
		color: white;
		margin-bottom: 80px;
	}

	.list-item-right {
		margin-right: 0;
	}
</style>