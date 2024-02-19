<script setup>
	import {usePatientStore} from '@/stores/Patient';

	const patientStore = usePatientStore()
</script>

<template>
	<nav>
		<div id="nav-trainer">
			{{ patientStore.patientCode }}
		</div>
		<div id="nav-exercise-code">
			{{ patientStore.areaName }}
		</div>
	</nav>
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
	</table>
</template>

<style scoped>
	nav {
		width: 100%;
		height: 60px;
		display: flex;
		float: left;
	}

	#nav-trainer, #nav-exercise-code {
		width: 50%;
		height: 100%;
		border-bottom: 8px solid black;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.5em;
	}

	#nav-trainer {
		border-right: 4px solid black;
	}

	#nav-exercise-code {
		border-left: 4px solid black;
	}

	table{
		border-collapse: collapse;
		width: 100%;
	}

	td{
		width: 50%;
		padding: 10px;
	}

	.key{
		font-weight: bold;
	}
</style>