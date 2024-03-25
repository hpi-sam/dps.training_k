<script setup lang="ts">
	import {ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient'
	import {Modules, setModule, showErrorToast} from "@/App.vue"
	import {svg} from "@/assets/Svg"

	const exerciseIdInput = ref("")
	const patientIdInput = ref("")

	function submit() {
		const patientStore = usePatientStore()

		const exerciseIdNumber = parseInt(exerciseIdInput.value)
		const patientIdNumber = parseInt(patientIdInput.value)

		if (isNaN(exerciseIdNumber) || isNaN(patientIdNumber)) {
			showErrorToast("Fehler: Übungs- oder Patienten-ID nicht numerisch")
			return
		}

		patientStore.patientID = patientIdNumber

		const requestBody = {
			"exerciseId": exerciseIdNumber,
			"patientId": patientIdNumber,
		}

		fetch('http://localhost:8000/patient/access', {
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
						case 401:
							showErrorToast("Fehler: falsche Übungs- oder Patienten-ID")
							break
						default:
							showErrorToast("Fehler: Server nicht erreichbar")
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
	}
</script>

<template>
	<div id="main">
		<div id="form">
			<h1>Patienten-Zugang</h1>
			<input v-model="exerciseIdInput" placeholder="Übungs-ID">
			<input v-model="patientIdInput" placeholder="Patienten-ID">
			<button @click="submit()">
				<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
					<path :d="svg.loginIcon" />
				</svg>
			</button>
		</div>
	</div>
</template>

<style scoped>
	@import url(../../assets/login.css);
</style>