<script setup lang="ts">
	import { ref } from 'vue'
	import { useAvailablesStore } from '@/stores/Availables'
	import ActionConfig from '@/components/widgets/ActionConfig.vue'
	import {svg} from '@/assets/Svg'

	const emit = defineEmits(['close-action-selection'])

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
	<ActionConfig
		v-if="showAction"
		:current-action="currentAction"
		@close-action="showAction=false"
	/>
	<div v-if="!showAction" class="flex-container">
		<h1>Wähle eine Aktion</h1>
		<button class="close-button" @click="emit('close-action-selection')">
			<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
				<path :d="svg.closeIcon" />
			</svg>
		</button>
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