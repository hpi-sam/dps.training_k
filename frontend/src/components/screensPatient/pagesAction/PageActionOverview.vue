<script setup lang="ts">
	import {useActionOverviewStore} from '@/stores/ActionOverview'
	import {computed, ref} from 'vue'
	import {svg} from '@/assets/Svg'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import socketPatient from '@/sockets/SocketPatient'
	import ResultPopup from '@/components/widgets/ResultPopup.vue'

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
			case 'PL':
				return svg.waitingIcon
			case 'OH':
				return svg.blockIcon
		}
	}

	const currentActionId = ref(Number.NEGATIVE_INFINITY)
	const currentActionName = ref('No Action Name')
	const currentActionResult = ref('No Action Result')

	const showDeletePopup = ref(false)
	const showResultPopup = ref(false)

	function deleteAction() {
		socketPatient.deleteAction(currentActionId.value)
		showDeletePopup.value = false
	}

	function openDeletePopup(actionName: string) {
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
	<h1>Übersicht</h1>
	<div class="scroll">
		<div class="list">
			<button class="listItemAddButton" @click="emit('add-action')">
				Aktion hinzufügen
			</button>
			<div
				v-for="action in actionsNotFinished"
				:key="action.actionId"
				class="listItem"
			>
				<button class="listItemButton" @click="openDeletePopup(action.actionName)">
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="getIconPath(action.actionStatus)" />
						</svg>
					</div>
					<div class="listItemName">
						{{ action.actionName }}
					</div>
					<div class="time">
						{{ new Date(new Date(0).setSeconds(action.timeUntilCompletion)).toISOString().substring(14, 19) }}
					</div>
				</button>
			</div>
		</div>
		<div v-if="actionsInEffect.length" class="list">
			<p>Wirkende Effekte</p>
			<div
				v-for="action in actionsInEffect"
				:key="action.actionId"
				class="listItem"
			>
				<button class="listItemButton" @click="openResultPopup(action.actionName, action.actionResult)">
					<div class="listItemName">
						{{ action.actionName }}
					</div>
					<div v-if="action.timeUntilCompletion > 0" class="time">
						{{ new Date(new Date(0).setSeconds(action.timeUntilCompletion)).toISOString().substring(14, 19) }}
					</div>
				</button>
			</div>
		</div>
		<div v-if="actionsFinished.length" class="list">
			<p>Abgeschlossene Aktionen</p>
			<div
				v-for="action in actionsFinished"
				:key="action.actionId"
				class="listItem"
			>
				<button class="listItemButton" @click="openResultPopup(action.actionName, action.actionResult)">
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="getIconPath(action.actionStatus)" />
						</svg>
					</div>
					<div class="listItemName">
						{{ action.actionName }}
					</div>
					<div v-if="action.actionResult" class="time">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="svg.descriptionIcon" />
						</svg>
					</div>
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.time {
		margin-left: auto;
		margin-right: 16px;
	}
</style>