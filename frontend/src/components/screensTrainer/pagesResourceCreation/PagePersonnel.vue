<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'
	import PersonnelPopup from '@/components/widgets/PersonnelPopup.vue'
	import socketTrainer from '@/sockets/SocketTrainer'

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
</script>

<template>
	<PersonnelPopup v-if="showPopup" :personnel-id="currentPersonnel" @close-popup="showPopup=false" />
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