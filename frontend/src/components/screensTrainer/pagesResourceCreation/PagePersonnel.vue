<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from '@/sockets/SocketTrainer'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemRight} from "@/components/widgets/List"
	import IconButton from '@/components/widgets/IconButton.vue'
	import {svg} from "@/assets/Svg"
	import RenamePopup from '@/components/widgets/RenamePopup.vue'
	import { generateName } from '@/utils'

	const props = defineProps({
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const currentPersonnel = ref(Number.NEGATIVE_INFINITY)
	const currentPersonnelName = computed(() => exerciseStore.getPersonnel(currentPersonnel.value)?.personnelName)

	const showRenamePopup = ref(false)
	const showDeletePopup = ref(false)

	function openRenamePopup(personnelId: number) {
		currentPersonnel.value = personnelId
		showRenamePopup.value = true
	}

	function openDeletePopup(personnelId: number) {
		currentPersonnel.value = personnelId
		showDeletePopup.value = true
	}

	function addPersonnel() {
		socketTrainer.personnelAdd(props.currentArea, generateName())
	}

	function deletePersonnel() {
		socketTrainer.personnelDelete(currentPersonnel.value)
	}

	function renamePersonnel(name: string) {
		socketTrainer.personnelRename(currentPersonnel.value, name)
	}
</script>

<template>
	<RenamePopup
		v-if="showRenamePopup"
		:name="currentPersonnelName || ''"
		:title="'Personal umbenennen'"
		@close-popup="showRenamePopup=false"
		@rename="(name) => renamePersonnel(name)"
	/>
	<DeleteItemPopup
		v-if="showDeletePopup"
		:name="exerciseStore.getPersonnel(currentPersonnel)?.personnelName"
		@close-popup="showDeletePopup=false"
		@delete="deletePersonnel"
	/>
	<h1>Personal</h1>
	<CustomList>
		<ListItemAddButton v-if="currentAreaData" text="Personal hinzufügen" @click="addPersonnel()" />
		<ListItem
			v-for="personnel in currentAreaData?.personnel"
			:key="personnel.personnelName"
		>
			<ListItemButton>
				<ListItemName :name="personnel.personnelName" />
				<ListItemRight>
					<IconButton :icon="svg.penIcon" @click="openRenamePopup(personnel.personnelId)" />
					<IconButton :icon="svg.binIcon" @click="openDeletePopup(personnel.personnelId)" />
				</ListItemRight>
			</ListItemButton>
		</ListItem>
	</CustomList>
</template>