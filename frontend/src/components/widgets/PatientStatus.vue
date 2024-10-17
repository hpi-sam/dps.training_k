<script setup lang="ts">
	import {usePatientStore} from '@/stores/Patient'
	import {useContinuousVariablesStore} from "@/stores/ContinuousVariables"
	import {computed} from "vue"
	import {strings} from "@/strings"
	import {ContinuousVariableName} from "@/enums"

	const patientStore = usePatientStore()
	const continuousStateStore = useContinuousVariablesStore()

	const breathing = computed(() => {
		const spo2Val = continuousStateStore.getCurrentValueByName(ContinuousVariableName.SPO2)?.toFixed(0)
		return patientStore.breathing.replace(/(SpO2: )\d+/, `$1${spo2Val}`)
	})

	const circulation = computed(() => {
		const heartRateVal = continuousStateStore.getCurrentValueByName(ContinuousVariableName.HEART_RATE)?.toFixed(0)
		return patientStore.circulation.replace(/(Herzfreq: )\d+/, `$1${heartRateVal}`)
	})

</script>

<template>
	<table>
		<tr>
			<td colspan="2">
				<hr>
				<h1>{{ strings.patientState.title }}</h1>
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					{{ strings.patientState.airway }}
				</p>{{ patientStore.airway }}
			</td>
			<td>
				<p class="key">
					{{ strings.patientState.breathing }}
				</p>{{ breathing }}
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					{{ strings.patientState.circulation }}
				</p>{{ circulation }}
			</td>
			<td>
				<p class="key">
					{{ strings.patientState.consciousness }}
				</p>{{ patientStore.consciousness }}
			</td>
		</tr>
		<tr>
			<td>
				<p class="key">
					{{ strings.patientState.psyche }}
				</p>{{ patientStore.psyche }}
			</td>
			<td>
				<p class="key">
					{{ strings.patientState.skin }}
				</p>{{ patientStore.skin }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<hr>
				<h1>
					{{ strings.patientInfo.title }}
				</h1>
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.injury }}
				</p>{{ patientStore.injury }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.mobility }}
				</p>{{ patientStore.mobility }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.preexistingIllnesses }}
				</p>{{ patientStore.preexistingIllnesses }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.permanentMedication }}
				</p>{{ patientStore.permanentMedication }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.currentCaseHistory }}
				</p>{{ patientStore.currentCaseHistory }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.pretreatment }}
				</p>{{ patientStore.pretreatment }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.biometrics }}
				</p>{{ patientStore.biometrics }}
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<p class="key">
					{{ strings.patientInfo.patientId }}
				</p>{{ patientStore.patientId }}
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