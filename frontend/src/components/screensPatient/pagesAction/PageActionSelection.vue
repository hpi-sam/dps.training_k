<script setup lang="ts">
	import {ref} from 'vue'
	import {useAvailablesStore} from '@/stores/Availables'
	import CloseButton from '@/components/widgets/CloseButton.vue'
	import socketPatient from '@/sockets/SocketPatient'
	import { useActionCheckStore } from '@/stores/ActionCheck'
	import { Pages } from '../ScreenActions.vue'

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
		/*
		actionCheckStore.$reset()
		socketPatient.actionCheck(actionName)
		currentAction.value = actionName
		emit('set-page', Pages.ACTION_CHECK)
		*/
		// this is a hotfix until the action check is implemented in backend
		socketPatient.actionAdd(actionName)
	}
</script>
<template>
	<div class="flex-container">
		<div class="scroll">
			<h1>Wähle eine Aktion</h1>
			<CloseButton @click="emit('close-action-selection')" />
			<div
				v-for="actionTyp in availablesStore.getActionCategories"
				:key="actionTyp"
				class="list"
			>
				<h2>{{ getTypeLabel(actionTyp) }}</h2>
				<div
					v-for="action in filteredActions(actionTyp)"
					:key="action.actionName"
					class="listItem"
				>
					<button class="listItemButton" @click="openAction(action.actionName)">
						<div class="listItemName">
							{{ action.actionName }}
						</div>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>
<style scoped>
	h1 {
		text-align: center;
		margin-top: 30px;
	}
</style>