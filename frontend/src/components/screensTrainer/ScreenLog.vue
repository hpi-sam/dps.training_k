<script setup lang="ts">
	import {useLogStore} from "@/stores/Log"
	import LogPopup from "../widgets/LogPopup.vue"
	import {ref} from "vue"
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemLeft} from "@/components/widgets/List"

	const logStore = useLogStore()

	const currentLogId = ref(Number.NEGATIVE_INFINITY)

	function openPopup(logId: number) {
		currentLogId.value = logId
		showPopup.value = true
	}

	const showPopup = ref(false)
</script>

<template>
	<LogPopup v-if="showPopup" :log-id="currentLogId" @close-popup="showPopup=false" />
	<div class="flex-container">
		<div class="scroll">
			<h1>Log</h1>
			<CustomList>
				<h2 v-if="!logStore.log.length">
					Keine Log-Einträge vorhanden
				</h2>
				<ListItem
					v-for="logEntry in logStore.log"
					:key="logEntry.logId"
				>
					<ListItemButton @click="openPopup(logEntry.logId)">
						<ListItemLeft>
							{{ new Date(logEntry.logTime).toTimeString().split(' ')[0] }}
						</ListItemLeft>
						&#x2223;
						<ListItemName :name="logEntry.logMessage || 'Keine Nachricht'" />
					</ListItemButton>
				</ListItem>
			</CustomList>
		</div>
	</div>
</template>

<style scoped>
	.list-item-left {
		margin-right: 16px;
	}
</style>