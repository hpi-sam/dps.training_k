<script setup lang="ts">
	import { computed } from "vue"
    import { useLogStore } from '@/stores/Log'
	import CloseButton from "./CloseButton.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		logId: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const logStore = useLogStore()

	const currentLogEntry = computed(() => {
		if (props.logId !== Number.NEGATIVE_INFINITY && logStore.getLogEntry(props.logId)) {
			return logStore.getLogEntry(props.logId)
		}
		return null
	})
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<h2>
				Log-Eintrag
			</h2>
			<table>
				<tr>
					<td class="key">
						Zeitpunkt:
					</td>
					<td>
						{{ new Date(currentLogEntry?.logTime || '').toTimeString().split(' ')[0] }}
					</td>
				</tr>
				<tr>
					<td class="key">
						Bereich:
					</td>
					<td>
						{{ currentLogEntry?.areaName }}
					</td>
				</tr>
				<tr>
					<td class="key">
						Patient:
					</td>
					<td>
						{{ currentLogEntry?.patientId }}
					</td>
				</tr>
				<tr>
					<td class="key">
						Personal:
					</td>
					<td>
						{{ currentLogEntry?.personnelId }}
					</td>
				</tr>
			</table>
			<br>
			<p>
				{{ currentLogEntry?.logMessage }}
			</p>
			<br>
		</div>
	</div>
</template>

<style scoped>
	.popup {
		max-width: 50vw;
		overflow: hidden;
	}

	table {
		text-align: left;
	}
	
	.key {
		padding-right: 20px;
		font-weight: bold;
	}

	p {
		text-align: left;
	}
</style>