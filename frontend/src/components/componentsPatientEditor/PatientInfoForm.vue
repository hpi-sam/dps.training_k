<script setup lang="ts">
	import { getNode } from '@formkit/core'
	import { info } from '@/components/ModulePatientEditor.vue'
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
		type="form"
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
			:options="['nicht triagiert', 'schwarz', 'rot', 'gelb', 'grün']"
			validation="required"
		/>

		<FormKit
			id="sex"
			type="select"
			name="sex"
			label="Geschlecht"
			placeholder="Wähle ein Geschlecht"
			:options="['männlich', 'weiblich']"
			validation="required"
		/>

		<FormKit
			id="age"
			type="number"
			name="age"
			label="Alter"
			placeholder="Gib das Alter des Patienten ein"
			validation="required"
		/>

		<FormKit
			id="address"
			type="text"
			name="address"
			label="Adresse"
			placeholder="Straße Hausnummer, PLZ Ort"
			validation="required"
		/>

		<FormKit
			id="injury"
			type="textarea"
			name="injury"
			label="Verletzung"
			placeholder="Beschreibe die Verletzung des Patienten"
			validation="required"
		/>

		<FormKit
			id="biometrics"
			type="textarea"
			name="biometrics"
			label="Biometrie"
			placeholder="Haarfarbe, Augenfarbe, Größe, Brille?"
			validation="required"
		/>

		<FormKit
			id="mobility"
			type="select"
			name="mobility"
			label="Mobilität"
			placeholder="Wähle die Mobilität"
			:options="['initial gefähig', 'initial bedingt gefähig', 'initial nicht gefähig', 'initial bettlägerig']"
			validation="required"
		/>

		<FormKit
			id="preexistingIllnesses"
			type="textarea"
			name="preexistingIllnesses"
			label="Vorerkrankungen"
			placeholder="Welche Vorerkrankungen besitzt der Patient?"
			validation="required"
		/>

		<FormKit
			id="permanentMedication"
			type="textarea"
			name="permanentMedication"
			label="Dauer-Medikation"
			placeholder="Gib die Dauer-Medikation des Patienten an"
			validation="required"
		/>

		<FormKit
			id="currentCaseHistory"
			type="textarea"
			name="currentCaseHistory"
			label="Aktuelle Anamnese / Rettungsdienst-Übergabe"
			placeholder="Gib die Aktuelle Anamnese / Rettungsdienst-Übergabe des Patienten an"
			validation="required"
		/>

		<FormKit
			id="pretreatment"
			type="textarea"
			name="pretreatment"
			label="Vorbehandlung"
			placeholder="Wie wurde der Patient bereits behandelt?"
			validation="required"
		/>
	</FormKit>
</template>