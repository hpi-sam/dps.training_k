<script setup lang="ts">
	import { ref } from 'vue'
	import { useAvailablesStore } from '@/stores/Availables'
	import ActionConfig from '@/components/widgets/ActionConfig.vue'

	const availablesStore = useAvailablesStore()
	const availableActions = ref(availablesStore.actions)

	const currentAction = ref('Keine Aktion ausgewählt')

	function filteredActions(actionType: string) {
		return availableActions.value.filter(action => action.actionType === actionType)
	}

	function getTypeLabel(actionType: string) {
		switch (actionType) {
			case 'treatment':
				return 'Behandlung'
			case 'lab':
				return 'Labor'
			default:
				return 'Sonstiges'
		}
	}

	function openAction(actionName: string) {
		currentAction.value = actionName
		showAction.value = true
	}

	const showAction = ref(false)
</script>

<template>
	<ActionConfig v-if="showAction" :current-action="currentAction" @close-action="showAction=false" />
	<div v-if="!showAction">
		<h1>Wähle eine Aktion</h1>
		<div
			v-for="actionTyp in availablesStore.getActionTypes"
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
</template>

<style scoped>
	h1 {
		text-align: center;
		margin-top: 30px;
	}
</style>