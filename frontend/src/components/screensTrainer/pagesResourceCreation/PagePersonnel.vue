<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from '@/sockets/SocketTrainer'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton} from "@/components/widgets/List"

	const props = defineProps({
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const currentPersonnel = ref(Number.NEGATIVE_INFINITY)

	const showPopup = ref(false)

	function openPopup(personnelId: number) {
		currentPersonnel.value = personnelId
		showPopup.value = true
	}

	function addPersonnel() {
		socketTrainer.personnelAdd(props.currentArea)
	}

	function deletePersonnel() {
		socketTrainer.personnelDelete(currentPersonnel.value)
	}
</script>

<template>
	<DeleteItemPopup
		v-if="showPopup"
		:name="exerciseStore.getPersonnel(currentPersonnel)?.personnelName"
		@close-popup="showPopup=false"
		@delete="deletePersonnel"
	/>
	<h1>Personal</h1>
	<CustomList>
		<ListItemAddButton v-if="currentAreaData" text="Personal hinzufügen" @click="addPersonnel()" />
		<ListItem
			v-for="personnel in currentAreaData?.personnel"
			:key="personnel.personnelName"
		>
			<ListItemButton @click="openPopup(personnel.personnelId)">
				<ListItemName :name="personnel.personnelName" />
			</ListItemButton>
		</ListItem>
	</CustomList>
</template>