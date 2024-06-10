<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import socketTrainer from '@/sockets/SocketTrainer'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemRight} from "@/components/widgets/List"
	import BinButton from '@/components/widgets/BinButton.vue'

	const props = defineProps({
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const currentPersonnel = ref(Number.NEGATIVE_INFINITY)

	const showDeletePopup = ref(false)

	function openDeletePopup(personnelId: number) {
		currentPersonnel.value = personnelId
		showDeletePopup.value = true
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
					<BinButton @click="openDeletePopup(personnel.personnelId)" />
				</ListItemRight>
			</ListItemButton>
		</ListItem>
	</CustomList>
</template>