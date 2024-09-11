<script setup lang="ts">
	import { getNode } from '@formkit/core'
	import { info } from '@/components/screensTrainer/ScreenPatientEditor.vue'
	import { watch } from 'vue'
	
	watch(
		info,
		(newVal) => {
			const patientInfoFormNode = getNode('patientInfoForm')
			patientInfoFormNode?.input(newVal)
		}
	)
</script>

<template>
	<h1>Patient</h1>
	<FormKit
		id="patientInfoForm"
		v-slot="{ disabled }"
		type="form"
		:actions="false"
	>
		<FormKit
			id="code"
			type="number"
			name="code"
			label="Code"
			placeholder="Ein neuer Code zwischen 2001 und 9999"
			validation="required|number|between:2001,9999"
		/>

		<FormKit
			id="triage"
			type="select"
			name="triage"
			label="Start-Triage"
			placeholder="Wähle die Start-Triage"
			:options="[
				{ value: '-', label: 'nicht triagiert' },
				{ value: '1', label: 'rot' },
				{ value: '2', label: 'gelb' },
				{ value: '3', label: 'grün' },
				{ value: 'X', label: 'schwarz' }
			]"
		/>

		<FormKit
			id="personalDetails"
			type="text"
			name="personalDetails"
			label="Personalien"
			placeholder="Name, Geburtsdatum, Adresse"
		/>

		<FormKit
			id="bloodType"
			type="select"
			name="bloodType"
			label="Blutgruppe"
			placeholder="Wähle die Blutgruppe"
			:options="[
				{ value: 1, label: 'B Rh pos' },
				{ value: 2, label: 'B Rh pos' },
				{ value: 3, label: 'A rh neg' },
				{ value: 4, label: '0 Rh pos' },
				{ value: 5, label: 'B rh neg' },
				{ value: 6, label: 'AB rh neg' },
				{ value: 7, label: 'O rh neg' },
				{ value: 8, label: 'AB Rh pos' }
			]"
		/>

		<FormKit
			id="injury"
			type="textarea"
			name="injury"
			label="Verletzung"
			placeholder="Beschreibe die Verletzung des Patienten"
		/>

		<FormKit
			id="biometrics"
			type="textarea"
			name="biometrics"
			label="Biometrie"
			placeholder="Geschlecht, Alter, Haarfarbe, Augenfarbe, Größe, Brille?"
		/>

		<FormKit
			id="mobility"
			type="select"
			name="mobility"
			label="Mobilität"
			placeholder="Wähle die Mobilität"
			:options="['initial gefähig', 'initial bedingt gefähig', 'initial nicht gefähig', 'initial bettlägerig']"
		/>

		<FormKit
			id="preexistingIllnesses"
			type="textarea"
			name="preexistingIllnesses"
			label="Vorerkrankungen"
			placeholder="Welche Vorerkrankungen besitzt der Patient?"
		/>

		<FormKit
			id="permanentMedication"
			type="textarea"
			name="permanentMedication"
			label="Dauer-Medikation"
			placeholder="Gib die Dauer-Medikation des Patienten an"
		/>

		<FormKit
			id="currentCaseHistory"
			type="textarea"
			name="currentCaseHistory"
			label="Aktuelle Anamnese / Rettungsdienst-Übergabe"
			placeholder="Gib die Aktuelle Anamnese / Rettungsdienst-Übergabe des Patienten an"
		/>

		<FormKit
			id="pretreatment"
			type="textarea"
			name="pretreatment"
			label="Vorbehandlung"
			placeholder="Wie wurde der Patient bereits behandelt?"
		/>

		<FormKit
			id="op"
			type="textarea"
			name="op"
			label="OP / Interventions-Verlauf"
			placeholder="Wie verläuft die OP / Intervention?"
		/>
	</FormKit>
</template>