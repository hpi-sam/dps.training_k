<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'
	import socketTrainer from '@/sockets/SocketTrainer'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'

	const emit = defineEmits(['add-action'])
</script>

<template>
	<h1>Übersicht</h1>
	<div class="list">
		<!--<div
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
		</div>-->
		<button class="listItemAddButton" @click="emit('add-action')">
			Aktion hinzufügen
		</button>
	</div>
</template>