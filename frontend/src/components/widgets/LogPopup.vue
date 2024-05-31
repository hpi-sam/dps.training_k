<script setup lang="ts">
	import {computed} from "vue"
	import {useLogStore} from '@/stores/Log'
	import CloseButton from "./CloseButton.vue"
	import {useExerciseStore} from "../../stores/Exercise"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		logId: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const logStore = useLogStore()
	const exerciseStore = useExerciseStore()

	const currentLogEntry = computed(() => {
		if (props.logId !== Number.NEGATIVE_INFINITY && logStore.getLogEntry(props.logId)) {
			return logStore.getLogEntry(props.logId)
		}
		return null
	})

	const patientName = computed(() => {
		if (currentLogEntry.value?.patientId) {
			const store = useExerciseStore()
			const patient = store.getPatient(currentLogEntry.value.patientId)
			return patient ? patient.patientName : ''
		}
		return ''
	})

	const personnelNames = computed(() => {
		let names = ''
		if (currentLogEntry.value?.personnelIds) {
			const store = useExerciseStore()
			for (const personnelId of currentLogEntry.value.personnelIds) {
				if (names !== '') names = names + ', '
				names = names + store.getPersonnel(personnelId)?.personnelName
			}
		}
		return names
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
				<tr v-if="currentLogEntry?.logTime">
					<td class="key">
						Zeitpunkt:
					</td>
					<td>
						{{ new Date(currentLogEntry?.logTime || '').toTimeString().split(' ')[0] }}
					</td>
				</tr>
				<tr v-if="currentLogEntry?.areaId">
					<td class="key">
						Bereich:
					</td>
					<td>
						{{ exerciseStore.getAreaName(currentLogEntry?.areaId) }}
					</td>
				</tr>
				<tr v-if="currentLogEntry?.patientId">
					<td class="key">
						Patient:
					</td>
					<td>
						{{ currentLogEntry?.patientId }} {{ patientName }}
					</td>
				</tr>
				<tr v-if="currentLogEntry?.personnelIds?.length">
					<td class="key">
						Personal:
					</td>
					<td>
						{{ personnelNames }}
					</td>
				</tr>
				<tr v-if="currentLogEntry?.materialNames?.length">
					<td class="key">
						Material:
					</td>
					<td>
						{{ currentLogEntry?.materialNames.join(', ') }}
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
		min-width: 300px;
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