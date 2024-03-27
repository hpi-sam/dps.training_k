<script setup lang="ts">
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
	import {useLogStore} from "@/stores/Log"

	const logStore = useLogStore()
</script>

<template>
	<TopBarTrainer />
	<h1>Log</h1>
	<div class="list">
		<div
			v-for="logEntry in logStore.log"
			:key="logEntry.logTime.toString()"
			class="listItem"
		>
			<button class="listItemButton">
				<div class="listItemName">
					{{ new Date(logEntry.logTime).toTimeString().split(' ')[0] }}
				</div>
				I
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