<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'
	import { computed, ref } from 'vue'
	import CloseButton from './CloseButton.vue'
	import { useActionCheckStore } from '@/stores/ActionCheck'
	import { svg } from '@/assets/Svg'	
	import ActionGroupPopup from './ActionGroupPopup.vue'

	const emit = defineEmits(['close-action'])

	const props = defineProps({
		currentAction: {
			type: String,
			default: "Kein Name angegeben"
		}
	})

	function addAction() {
		socketPatient.actionAdd(props.currentAction)
		newActionsAllowed.value = false
		emit('close-action')
	}

	const actionCheckStore = useActionCheckStore()

	const errorMessage = ref(computed(() => {
		if (actionCheckStore.prohibitedActions.length > 0) {
			return "Eine durchgeführte Aktion verhindert die Anordnung."
		} else if (actionCheckStore.requiredActions.singleActions.length > 0 || actionCheckStore.requiredActions.actionGroups.length > 0) {
			return "Es müssen zuerst andere Aktionen durchgeführt werden."
		} else if (!newActionsAllowed.value) {
			return "Warte, bis wieder neue Aktionen angeordnet werden können."
		} else {
			return ""
		}
	}))

	function getIconPath(available: number, assigned: number, needed: number) {
		if (assigned < needed) {
			return svg.blockIcon
		} else if (available < needed) {
			return svg.waitingIcon
		} else {
			return svg.playIcon
		}
	}

	function openActionGroupPopup(actions: string[]) {
		actionsOfGroup.value = actions
		showActionGroupPopup.value = true
	}

	const showActionGroupPopup = ref(false)
	const actionsOfGroup = ref([] as string[])
</script>
<script lang="ts">
	const newActionsAllowed = ref(true)

	export function allowNewActions() {
		newActionsAllowed.value = true
	}
</script>

<template>
	<ActionGroupPopup
		v-if="showActionGroupPopup"
		:actions="actionsOfGroup"
		@close-popup="showActionGroupPopup=false"
	/>
	<div class="flex-container">
		<div>
			<CloseButton @close="emit('close-action')" />
		</div>
		<div class="scroll">
			<h1>{{ props.currentAction }}</h1>
			<div class="list">
				<p>
					Ausführungsdauer: {{ new Date(new Date(0).setSeconds(actionCheckStore.applicationDuration)).toISOString().substring(14, 19) }}
				</p>
				<p v-if="actionCheckStore.effectDuration > 0">
					Effektdauer: {{ new Date(new Date(0).setSeconds(actionCheckStore.effectDuration)).toISOString().substring(14, 19) }}
				</p>
				<br>
				Personal
				<div
					v-for="personnel in actionCheckStore.personnel"
					:key="personnel.name"
					class="listItem"
				>
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="getIconPath(personnel.available, personnel.assigned, personnel.needed)" />
						</svg>
					</div>
					<div class="listItemButton">
						<div class="listItemName">
							{{ personnel.name }}
						</div>
						<div class="rightText">
							{{ personnel.available }} / {{ personnel.assigned }} / {{ personnel.needed }}
						</div>
					</div>
				</div>
				<br>Material
				<div
					v-for="material in actionCheckStore.material"
					:key="material.name"
					class="listItem"
				>
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="getIconPath(material.available, material.assigned, material.needed)" />
						</svg>
					</div>
					<div class="listItemButton">
						<div class="listItemName">
							{{ material.name }}
						</div>
						<div class="rightText">
							{{ material.available }} / {{ material.assigned }} / {{ material.needed }}
						</div>
					</div>
				</div>
				<br>Laborgeräte
				<div
					v-for="labDevice in actionCheckStore.labDevices"
					:key="labDevice.name"
					class="listItem"
				>
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="getIconPath(labDevice.available, labDevice.available, labDevice.needed)" />
						</svg>
					</div>
					<div class="listItemButton">
						<div class="listItemName">
							{{ labDevice.name }}
						</div>
						<div class="rightText">
							{{ labDevice.available }} / {{ labDevice.needed }}
						</div>
					</div>
				</div>
				<br>Folgende Aktionen müssen zuvor durchgeführt werden
				<div
					v-for="(action, index) in actionCheckStore.requiredActions.singleActions"
					:key="index"
					class="listItem"
				>
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="svg.closeIcon" />
						</svg>
					</div>
					<div class="listItemButton">
						<div class="listItemName">
							{{ action }}
						</div>
					</div>
				</div>
				<div
					v-for="(actionGroup, index) in actionCheckStore.requiredActions.actionGroups"
					:key="index"
					class="listItem"
				>
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="svg.closeIcon" />
						</svg>
					</div>
					<div class="listItemButton" @click="openActionGroupPopup(actionGroup.actions)">
						<div class="listItemName">
							{{ actionGroup.groupName ? actionGroup.groupName : actionGroup.actions.join(' / ') }}
						</div>
					</div>
				</div>
				<br>Folgende durchgeführte Aktionen verhindern die Anordnung
				<div
					v-for="(action, index) in actionCheckStore.prohibitedActions"
					:key="index"
					class="listItem"
				>
					<div class="listItemIcon">
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
							<path :d="svg.closeIcon" />
						</svg>
					</div>
					<div class="listItemButton">
						<div class="listItemName">
							{{ action }}
						</div>
					</div>
				</div>
			</div>
		</div>
		<div>
			<button class="main-button" :disabled="errorMessage.length > 0" @click="addAction()">
				Aktion anordnen
				<p v-if="errorMessage" class="error-message">
					{{ errorMessage }}
				</p>
			</button>
		</div>
	</div>
</template>

<style scoped>
	.main-button {
		background-color: var(--green);
		color: white;
	}

	.main-button:disabled {
		background-color: var(--gray);
	}

	.scroll {
		margin-bottom: 80px;
	}

	.rightText {
		margin-left: auto;
		margin-right: 16px;
		min-width: fit-content
	}

	.error-message {
		font-size: 12px;
	}
</style>