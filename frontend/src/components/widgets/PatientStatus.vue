<script setup lang="ts">
	import {usePatientStore} from '@/stores/Patient'

	const patientStore = usePatientStore()
</script>

<template>
	<table>
		<tr>
			<td colspan="2">
				<hr>
				<h1>
					Status
				</h1>
			</td>
		</tr>
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
			<td colspan="2">
				<hr>
				<h1>
					Info
				</h1>
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
		<tr>
			<td colspan="2">
				<hr>
			</td>
		</tr>
	</table>
</template>

<style scoped>
	table {
		border-collapse: collapse;
		width: 90%;
		max-width: calc(100% - 60px);
		table-layout: fixed;
		margin: 30px auto;
	}

	td {
		padding: 10px;
		vertical-align: top;
		overflow: hidden;
	}

	.key {
		font-weight: bold;
	}
</style>