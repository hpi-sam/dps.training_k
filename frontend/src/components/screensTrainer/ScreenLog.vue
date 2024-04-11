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
	<TopBarTrainer />
	<h1>Log</h1>
	<div class="list">
		<div
			v-for="logEntry in logStore.log"
			:key="logEntry.logId"
			class="listItem"
		>
			<button class="listItemButton" @click="openPopup(logEntry.logId)">
				<div class="listItemId">
					{{ new Date(logEntry.logTime).toTimeString().split(' ')[0] }}
				</div>
				&#x2223;
				<div class="listItemName">
					{{ logEntry.logMessage }}
				</div>
			</button>
		</div>
		<h2 v-if="!logStore.log.length">
			Keine Log-Einträge vorhanden
		</h2>
	</div>
</template>
<style scoped>
	h1 {
		text-align: center;
		margin-top: 90px;
	}
	h2 {
		text-align: center;
	}
</style>