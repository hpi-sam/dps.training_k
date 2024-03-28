<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'
	import socketTrainer from '@/sockets/SocketTrainer'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'

    const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
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

	function deletePersonnel(){
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
	<div class="list">
		<div
			v-for="personnel in currentAreaData?.personnel"
			:key="personnel.personnelName"
			class="listItem"
		>
			<button class="listItemButton" @click="openPopup(personnel.personnelId)">
				<div class="listItemName">
					{{ personnel.personnelName }}
				</div>
			</button>
			<ToggleSwitchForListItems default="active" />
		</div>
		<button v-if="currentAreaData" class="listItemAddButton" @click="addPersonnel()">
			Personal hinzufügen
		</button>
	</div>
</template>

<style scoped>
</style>