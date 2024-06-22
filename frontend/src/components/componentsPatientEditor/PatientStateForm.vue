<script setup>
const castRangeToNumber = (node) => {
  // We add a check to add the cast only to range inputs
  if (node.props.type !== 'range') return

  node.hook.input((value, next) => next(Number(value)))
}

const createPatient = async (fields) => {
  await new Promise((r) => setTimeout(r, 1000))
  alert(JSON.stringify(fields))
}
</script>

<template>
	<h1>Zustand</h1>
	<FormKit
		v-slot="{ value }"
		type="form"
		:plugins="[castRangeToNumber]"
		submit-label="Patient erstellen"
		@submit="createPatient"
	>
		<FormKit
			id="airway"
			name="airway"
			type="select"
			label="Atemwege"
			placeholder="Wähle den Zustand der Atemwege"
			:options="['freie Atemwege', 'künstlicher Atemweg', 'Atemwegsverlegung']"
			validation="required"
		/>

		<FormKit
			id="breathingRate"
			name="breathingRate"
			type="number"
			label="Atemfrequenz"
			placeholder="Atemzüge pro Minute"
			validation="required|min:0"
		/>

		<FormKit
			id="oxygenSaturation"
			name="oxygenSaturation"
			type="number"
			label="Sauerstoffsättigung"
			placeholder="SpO2 in %"
			validation="required|min:0"
		/>

		<FormKit
			id="breathing"
			name="breathing"
			type="select"
			label="Atmung"
			placeholder="Wähle den Zustand der Atmung"
			:options="['normale Atmung', 'vertiefte Atmung', 'flache Atmung', 'Beatmung', 'Atemstillstand']"
		/>

		<FormKit
			id="breathingSound"
			name="breathingSound"
			type="checkbox"
			label="Giemen und Brummen"
		/>

		<FormKit
			id="breathingLoudness"
			name="breathingLoudness"
			type="select"
			label="Atemgeräusche"
			placeholder="Sind Atemgeräusche hörbar?"
			:options="['normales AG hörbar', 'sehr leises AG hörbar', 'nur einseitiges AG hörbar', 'kein AG hörbar']"
		/>

		<FormKit
			id="heartRate"
			name="heartRate"
			type="number"
			label="Herzfrequenz"
			placeholder="Herzschläge pro Minute"
			validation="required|min:0"
		/>
		<pre wrap>{{ value }}</pre>
	</FormKit>
</template>