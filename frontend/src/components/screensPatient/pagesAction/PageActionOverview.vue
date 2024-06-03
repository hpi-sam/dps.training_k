<script setup lang="ts">
	import {useActionOverviewStore} from '@/stores/ActionOverview'
	import {computed, ref} from 'vue'
	import {svg} from '@/assets/Svg'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import socketPatient from '@/sockets/SocketPatient'
	import ResultPopup from '@/components/widgets/ResultPopup.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemRight, ListItemLeft} from "@/components/widgets/List"

	const emit = defineEmits(['add-action', 'close-action-selection'])

	const actionOverviewStore = useActionOverviewStore()

	const actions = computed(() => actionOverviewStore.actions)

	const actionsFinished = computed(() => actions.value.filter(
		action => action.actionStatus === 'FI' || action.actionStatus === 'EX'
	))

	const actionsInEffect = computed(() => actions.value.filter(
		action => action.actionStatus === 'IE'
	))

	const actionsNotFinished = computed(() => actions.value.filter(
		action => action.actionStatus === 'IP' || action.actionStatus === 'PL' || action.actionStatus === 'OH'
	))

	const getIconPath = (status: string) => {
		switch (status) {
			case 'IP':
				return svg.playIcon
			case 'FI':
			case 'EX':
				return svg.checkIcon
			case 'PL':
				return svg.waitingIcon
			case 'OH':
				return svg.blockIcon
			case 'IE':
				return svg.clockIcon
		}
	}

	const currentActionId = ref(Number.NEGATIVE_INFINITY)
	const currentActionName = ref('No Action Name')
	const currentActionResult = ref('No Action Result')

	const showDeletePopup = ref(false)
	const showResultPopup = ref(false)

	function deleteAction() {
		socketPatient.cancelAction(currentActionId.value)
		showDeletePopup.value = false
	}

	function openDeletePopup(actionId: number, actionName: string) {
		currentActionId.value = actionId
		currentActionName.value = actionName
		showDeletePopup.value = true
	}

	function openResultPopup(actionName: string, actionResult: string) {
		currentActionName.value = actionName
		currentActionResult.value = actionResult
		if (actionResult) showResultPopup.value = true
	}

</script>

<template>
	<DeleteItemPopup
		v-if="showDeletePopup"
		:name="currentActionName"
		@delete="deleteAction"
		@close-popup="showDeletePopup=false"
	/>
	<ResultPopup
		v-if="showResultPopup"
		:name="currentActionName"
		:result="currentActionResult"
		@close-popup="showResultPopup=false"
	/>
	<div class="flex-container">
		<div class="scroll">
			<h1>Übersicht</h1>
			<CustomList>
				<ListItemAddButton text="Aktion hinzufügen" @click="emit('add-action')" />
			</CustomList>
			<CustomList v-if="actionsNotFinished.length">
				<ListItem
					v-for="action in actionsNotFinished"
					:key="action.actionId"
				>
					<ListItemButton @click="openDeletePopup(action.actionId, action.actionName)">
						<ListItemLeft>
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="getIconPath(action.actionStatus)" />
							</svg>
						</ListItemLeft>
						<ListItemName :name="action.actionName" />
						<ListItemRight>
							{{ new Date(new Date(0).setSeconds(action.timeUntilCompletion)).toISOString().substring(12, 19) }}
						</ListItemRight>
					</ListItemButton>
				</ListItem>
			</CustomList>
			<CustomList v-if="actionsInEffect.length">
				<p>Wirkende Effekte</p>
				<ListItem
					v-for="action in actionsInEffect"
					:key="action.actionId"
				>
					<ListItemButton @click="openResultPopup(action.actionName, action.actionResult)">
						<ListItemLeft>
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="getIconPath(action.actionStatus)" />
							</svg>
						</ListItemLeft>
						<ListItemName :name="action.actionName" />
						<ListItemRight v-if="action.timeUntilCompletion > 0">
							{{ new Date(new Date(0).setSeconds(action.timeUntilCompletion)).toISOString().substring(12, 19) }}
						</ListItemRight>
					</ListItemButton>
				</ListItem>
			</CustomList>
			<CustomList v-if="actionsFinished.length">
				<p>Abgeschlossene Aktionen</p>
				<ListItem
					v-for="action in actionsFinished"
					:key="action.actionId"
				>
					<ListItemButton @click="openResultPopup(action.actionName, action.actionResult)">
						<ListItemLeft>
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="getIconPath(action.actionStatus)" />
							</svg>
						</ListItemLeft>
						<ListItemName :name="action.actionName" />
						<ListItemRight v-if="action.actionResult">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="svg.descriptionIcon" />
							</svg>
						</ListItemRight>
					</ListItemButton>
				</ListItem>
			</CustomList>
		</div>
	</div>
</template>