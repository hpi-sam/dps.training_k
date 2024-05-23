<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'
	import {computed, ref} from 'vue'
	import CloseButton from '@/components/widgets/CloseButton.vue'
	import {useActionCheckStore} from '@/stores/ActionCheck'
	import {svg} from '@/assets/Svg'
	import ActionGroupPopup from '@/components/widgets/ActionGroupPopup.vue'

	const emit = defineEmits(['close-action'])

	const actionCheckStore = useActionCheckStore()

	function closeActionCheck() {
		socketPatient.stopActionCheck()
		emit('close-action')
	}

	function addAction() {
		socketPatient.actionAdd(actionCheckStore?.actionName)
		newActionsAllowed.value = false
		closeActionCheck()
	}

	const errorMessage = ref(computed(() => {
		if (actionCheckStore?.prohibitedActions?.length > 0) {
			return "Eine durchgeführte Aktion verhindert die Anordnung."
		} else if (actionCheckStore?.requiredActions?.singleActions?.length > 0 || actionCheckStore?.requiredActions?.actionGroups?.length > 0) {
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
			<CloseButton @close="closeActionCheck()" />
		</div>
		<div class="scroll">
			<h1>{{ actionCheckStore?.actionName }}</h1>
			<div class="list">
				<p v-if="actionCheckStore?.applicationDuration">
					Ausführungsdauer: {{ new Date(new Date(0).setSeconds(actionCheckStore?.applicationDuration)).toISOString().substring(14, 19) }}
				</p>
				<p v-if="actionCheckStore?.effectDuration > 0">
					Effektdauer: {{ new Date(new Date(0).setSeconds(actionCheckStore?.effectDuration)).toISOString().substring(14, 19) }}
				</p>
				<br>
				<p v-if="actionCheckStore?.personnel?.length > 0">
					Personal (verfügbar / zugeordnet / benötigt)
				</p>
				<div
					v-for="personnel in actionCheckStore?.personnel"
					:key="personnel.name"
					class="listItem"
				>
					<div class="list-item-button">
						<div class="list-item-icon">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="getIconPath(personnel.available, personnel.assigned, personnel.needed)" />
							</svg>
						</div>
						<div class="list-item-name">
							{{ personnel.name }}
						</div>
						<div class="right-text">
							{{ personnel.available }} / {{ personnel.assigned }} / {{ personnel.needed }}
						</div>
					</div>
				</div>
				<br>
				<p v-if="actionCheckStore?.material?.length > 0">
					Material (verfügbar / zugeordnet / benötigt)
				</p>
				<div
					v-for="material in actionCheckStore?.material"
					:key="material.name"
					class="listItem"
				>
					<div class="list-item-button">
						<div class="list-item-icon">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="getIconPath(material.available, material.assigned, material.needed)" />
							</svg>
						</div>
						<div class="list-item-name">
							{{ material.name }}
						</div>
						<div class="right-text">
							{{ material.available }} / {{ material.assigned }} / {{ material.needed }}
						</div>
					</div>
				</div>
				<br>
				<p v-if="actionCheckStore.labDevices?.length > 0">
					Laborgeräte (verfügbar / benötigt)
				</p>
				<div
					v-for="labDevice in actionCheckStore?.labDevices"
					:key="labDevice.name"
					class="listItem"
				>
					<div class="list-item-button">
						<div class="list-item-icon">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="getIconPath(labDevice.available, labDevice.available, labDevice.needed)" />
							</svg>
						</div>
						<div class="list-item-name">
							{{ labDevice.name }}
						</div>
						<div class="right-text">
							{{ labDevice.available }} / {{ labDevice.needed }}
						</div>
					</div>
				</div>
				<br>
				<p v-if="actionCheckStore?.requiredActions?.singleActions?.length > 0">
					Folgende Aktionen müssen zuvor durchgeführt werden
				</p>
				<div
					v-for="(action, index) in actionCheckStore?.requiredActions?.singleActions"
					:key="index"
					class="listItem"
				>
					<div class="list-item-button">
						<div class="list-item-icon">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="svg.closeIcon" />
							</svg>
						</div>
						<div class="list-item-name">
							{{ action }}
						</div>
					</div>
				</div>
				<div
					v-for="(actionGroup, index) in actionCheckStore?.requiredActions?.actionGroups"
					:key="index"
					class="list-item"
				>
					<div class="list-item-button" @click="openActionGroupPopup(actionGroup.actions)">
						<div class="list-item-icon">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="svg.closeIcon" />
							</svg>
						</div>
						<div class="list-item-name">
							{{ actionGroup.groupName ? actionGroup.groupName : actionGroup.actions.join(' / ') }}
						</div>
						<div class="right-text">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="svg.descriptionIcon" />
							</svg>
						</div>
					</div>
				</div>
				<br>
				<p v-if="actionCheckStore?.prohibitedActions?.length > 0">
					Folgende durchgeführte Aktionen verhindern die Anordnung
				</p>
				<div
					v-for="(action, index) in actionCheckStore?.prohibitedActions"
					:key="index"
					class="list-item"
				>
					<div class="list-item-button">
						<div class="list-item-icon">
							<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
								<path :d="svg.closeIcon" />
							</svg>
						</div>
						<div class="list-item-name">
							{{ action }}
						</div>
					</div>
				</div>
			</div>
		</div>
		<div>
			<button v-if="actionCheckStore?.actionName" class="main-button" :disabled="errorMessage.length > 0" @click="addAction()">
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

	.right-text {
		flex-shrink: 0;
		margin-right: 16px;
		white-space: nowrap;
		width: auto;
	}

	.error-message {
		font-size: 12px;
	}
</style>