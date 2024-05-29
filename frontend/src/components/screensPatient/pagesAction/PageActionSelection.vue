<script setup lang="ts">
	import {ref} from 'vue'
	import {useAvailablesStore} from '@/stores/Availables'
	import CloseButton from '@/components/widgets/CloseButton.vue'
	import socketPatient from '@/sockets/SocketPatient'
	import { useActionCheckStore } from '@/stores/ActionCheck'
	import { Pages } from '../ScreenActions.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName} from "@/components/widgets/List"

	const emit = defineEmits(['close-action-selection', 'set-page'])

	const availablesStore = useAvailablesStore()
	const availableActions = ref(availablesStore.actions)

	const currentAction = ref('Keine Aktion ausgewählt')

	function filteredActions(actionCategory: string) {
		return availableActions.value.filter(action => action.actionCategory === actionCategory)
	}

	function getTypeLabel(actionCategory: string) {
		switch (actionCategory) {
			case 'TR':
				return 'Behandlung'
			case 'EX':
				return 'Untersuchung'
			case 'LA':
				return 'Labor'
			default:
				return 'Sonstiges'
		}
	}

	const actionCheckStore = useActionCheckStore()

	function openAction(actionName: string) {
		actionCheckStore.$reset()
		socketPatient.actionCheck(actionName)
		currentAction.value = actionName
		emit('set-page', Pages.ACTION_CHECK)
	}
</script>
<template>
	<div class="flex-container">
		<div class="scroll">
			<h1>Wähle eine Aktion</h1>
			<CloseButton @click="emit('close-action-selection')" />
			<CustomList
				v-for="actionTyp in availablesStore.getActionCategories"
				:key="actionTyp"
			>
				<h2>{{ getTypeLabel(actionTyp) }}</h2>
				<ListItem
					v-for="action in filteredActions(actionTyp)"
					:key="action.actionName"
				>
					<ListItemButton @click="openAction(action.actionName)">
						<ListItemName :name="action.actionName" />
					</ListItemButton>
				</ListItem>
			</CustomList>
		</div>
	</div>
</template>