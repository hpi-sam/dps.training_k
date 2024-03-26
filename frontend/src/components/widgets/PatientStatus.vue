<script setup lang="ts">
	import {usePatientStore} from '@/stores/Patient'

	const patientStore = usePatientStore()
</script>

<template>
	<table>
		<tr>
			<td>
				<p class="key">
					Airway
				</p>{{ patientStore.airway }}
			</td>
			<td>
				<p class="key">
					Breathing
				</p>{{ patientStore.breathing }}
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					Circulation
				</p>{{ patientStore.circulation }}
			</td>
			<td>
				<p class="key">
					Consciousness
				</p>{{ patientStore.consciousness }}
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					Psyche
				</p>{{ patientStore.psyche }}
			</td>
			<td>
				<p class="key">
					Skin
				</p>{{ patientStore.skin }}
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					Verletzungen
				</p>{{ patientStore.injury }}
			</td>
			<td>
				<p class="key">
					Vorerkrankungen
				</p>{{ patientStore.history }}
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					Personalien
				</p>{{ patientStore.personalDetails }}
			</td>
			<td>
				<p class="key">
					Biometrie
				</p>{{ patientStore.biometrics }}
			</td>
		</tr>
	</table>
</template>

<style scoped>
	table {
		border-collapse: collapse;
		width: 100%;
		table-layout: fixed;
		margin: 90px 30px 30px 30px;
	}

	td {
		width: 50%;
		padding: 10px;
		vertical-align: top;
		overflow: hidden;
	}

	.key {
		font-weight: bold;
	}
</style>