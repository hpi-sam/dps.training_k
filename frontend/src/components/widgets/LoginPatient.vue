<script setup>
	import {ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient.js';
	import {setModule, showErrorToast} from "@/App.vue";

	const exerciseCodeInput = ref("")
	const patientCodeInput = ref("")

	function submit() {
		const requestBody = {
			"message-type": "patient-login",
			"exerciseCode": exerciseCodeInput.value,
			"patientCode": patientCodeInput.value,
		}

		fetch('https://b8ef4433-e891-4dd8-acee-7618425b3cbb.mock.pstmn.io', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(requestBody),
		})
			.then(response => {
				if (!response.ok) {
					console.log('Login failed:', response);
					switch (response.status) {
						case 401:
							showErrorToast("Fehler: falscher Nutzername oder falsches Passwort")
							break;
						default:
							showErrorToast("Fehler: Server nicht erreichbar")
							break;
					}
					return Promise.reject('Patient login failed with status ' + response.status);
				}
				return response.json();
			})
			.then(data => {
				usePatientStore().token = data.token
				setModule('ModulePatient')
			})
	}
</script>

<template>
	<div id="main">
		<div id="form">
			<h1>Patienten-Zugang</h1>
			<input v-model="exerciseCodeInput" placeholder="Übungscode">
			<input v-model="patientCodeInput" placeholder="Patientencode">
			<button @click="submit()">
				<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
					<!-- eslint-disable-next-line max-len, vue/max-len -->
					<path
						d="M480-120v-80h280v-560H480v-80h280q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H480Zm-80-160-55-58 102-102H120v-80h327L345-622l55-58 200 200-200 200Z"
					/>
				</svg>
			</button>
		</div>
	</div>
</template>

<style scoped>
	@import url(../../assets/login.css);
</style>