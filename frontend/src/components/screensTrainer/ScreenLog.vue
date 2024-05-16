<script setup lang="ts">
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {useLogStore} from "@/stores/Log"
	import LogPopup from "../widgets/LogPopup.vue"
	import {ref} from "vue"

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
		<TopBarTrainer />
		<h1>Log</h1>
		<div class="scroll">
			<div class="list">
				<div
					v-for="logEntry in logStore.log"
					:key="logEntry.logId"
					class="list-item"
				>
					<button class="list-item-button" @click="openPopup(logEntry.logId)">
						<div class="list-item-id">
							{{ new Date(logEntry.logTime).toTimeString().split(' ')[0] }}
						</div>
						&#x2223;
						<div class="list-item-name">
							{{ logEntry.logMessage }}
						</div>
					</button>
				</div>
				<h2 v-if="!logStore.log.length">
					Keine Log-Einträge vorhanden
				</h2>
			</div>
		</div>
	</div>
</template>