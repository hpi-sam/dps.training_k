<script setup lang="ts">
	import {ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient'
	import {Modules, setModule, showErrorToast} from "@/App.vue"

	const exerciseIdInput = ref("")
	const patientIdInput = ref("")

	function submit() {
		const patientStore = usePatientStore()

		const exerciseId = exerciseIdInput.value
		const patientIdNumber = parseInt(patientIdInput.value)

		if (isNaN(patientIdNumber)) {
			showErrorToast("Fehler: Patienten-ID nicht numerisch")
			return
		}

		const patientId = String(patientIdNumber).padStart(6, '0')

		patientStore.patientId = patientId

		const requestBody = {
			"exerciseId": exerciseId,
			"patientId": patientId,
		}

		fetch('http://' + import.meta.env.VITE_SERVER_URL + '/api/patient/access', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(requestBody),
		})
			.then(response => {
				if (!response.ok) {
					console.log('Login failed:', response)
					switch (response.status) {
						case 400:
							showErrorToast("Fehler: Übungs-ID und oder Patienten-ID nicht angegeben")
							break
						case 401:
							showErrorToast("Fehler: Falsche Übungs- oder Patienten-ID")
							break
						default:
							showErrorToast("Fehler: Unbekannter Fehler")
							break
					}
					return Promise.reject('Patient login failed with status ' + response.status)
				}
				return response.json()
			})
			.then(data => {
				usePatientStore().token = data.token
				setModule(Modules.PATIENT)
			})
			.catch(_ => {
				// Do nothing here, just catch the error to prevent unhandled Promise rejection as it is already handled above in the switch case
			})
	}
</script>

<template>
	<div id="main">
		<div id="form">
			<h1>Patienten-Zugang</h1>
			<input id="patient-login-exercise-id" v-model="exerciseIdInput" placeholder="Übungs-ID">
			<input id="patient-login-patient-id" v-model="patientIdInput" placeholder="Patienten-ID">
			<button id="patient-login" @click="submit()">
				Einloggen
			</button>
		</div>
	</div>
</template>

<style scoped>
	@import url(../../assets/login.css);
</style>