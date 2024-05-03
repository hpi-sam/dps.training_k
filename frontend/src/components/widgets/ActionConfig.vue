<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'
	import { computed, ref } from 'vue'
	import CloseButton from './CloseButton.vue'
	import { useActionCheckStore } from '@/stores/ActionCheck'

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
		} else if (actionCheckStore.personnel.some(personnel => personnel.needed > personnel.available)) {
			return "Es ist nicht genügend Personal verfügbar."
		} else if (actionCheckStore.material.some(material => material.needed > material.available)) {
			return "Es ist nicht genügend Material verfügbar."
		} else if (actionCheckStore.labDevices.some(labDevice => labDevice.needed > labDevice.available)) {
			return "Es sind nicht genügend Laborgeräte verfügbar."
		} else if (!newActionsAllowed.value) {
			return "Warte, bis wieder neue Aktionen angeordnet werden können."
		} else {
			return ""
		}
	}))

</script>
<script lang="ts">
	const newActionsAllowed = ref(true)

	export function allowNewActions() {
		newActionsAllowed.value = true
	}
</script>

<template>
	<div class="flex-container">
		<div>
			<CloseButton @close="emit('close-action')" />
		</div>
		<div class="scroll">
			<h1>{{ props.currentAction }}</h1>
			<div class="list">
				Personal
				<div
					v-for="personnel in actionCheckStore.personnel"
					:key="personnel.name"
					class="listItem"
				>
					<div class="listItemButton">
						<div class="listItemName">
							{{ personnel.name }}
						</div>
						<div class="listItemName right">
							{{ personnel.available }} / {{ personnel.assigned }} / {{ personnel.needed }}
						</div>
					</div>
				</div>
				<p><br>Material</p>
				<div
					v-for="material in actionCheckStore.material"
					:key="material.name"
					class="listItem"
				>
					<div class="listItemButton">
						<div class="listItemName">
							{{ material.name }}
						</div>
						<div class="listItemName right">
							{{ material.available }} / {{ material.assigned }} / {{ material.needed }}
						</div>
					</div>
				</div>
				<p><br>Laborgeräte</p>
				<div
					v-for="labDevice in actionCheckStore.labDevices"
					:key="labDevice.name"
					class="listItem"
				>
					<div class="listItemButton">
						<div class="listItemName">
							{{ labDevice.name }}
						</div>
						<div class="listItemName right">
							{{ labDevice.available }} / {{ labDevice.needed }}
						</div>
					</div>
				</div>
				<p><br>Folgende Aktionen müssen zuvor durchgeführt werden</p>
				<div
					v-for="(action, index) in actionCheckStore.requiredActions.singleActions"
					:key="index"
					class="listItem"
				>
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
					<div class="listItemButton">
						<div class="listItemName">
							{{ actionGroup.groupName }}
						</div>
					</div>
				</div>
				<p><br>Folgende durchgeführte Aktionen verhindern die Anordnung</p>
				<div
					v-for="(action, index) in actionCheckStore.prohibitedActions"
					:key="index"
					class="listItem"
				>
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
				<p v-if="errorMessage">
					{{ errorMessage }}
				</p>
			</button>
		</div>
	</div>
</template>

<style scoped>
	.waiting-text {
		text-align: center;
		margin-top: 10px;
		margin-bottom: 70px;
	}

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

	.right {
		margin-left: auto;
		display: flex;
	}

	p {
		font-size: 12px;
	}
</style>