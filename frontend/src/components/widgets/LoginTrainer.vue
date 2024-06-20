<script setup lang="ts">
	import {ref} from 'vue'
	import {useTrainerStore} from '@/stores/Trainer'
	import {Modules, setModule, showErrorToast} from "@/App.vue"

	const usernameInput = ref("")
	const passwordInput = ref("")

	function submit() {
		const trainerStore = useTrainerStore()
		const username = usernameInput.value
		const password = passwordInput.value
		trainerStore.username = username

		const requestBody = {
			"username": username,
			"password": password,
		}

		fetch('http://' + import.meta.env.VITE_SERVER_URL + ':8000/trainer/login', {
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
							showErrorToast("Fehler: Username und oder Passwort nicht angegeben")
							break
						case 401:
							showErrorToast("Fehler: Falsches Passwort")
							break
						default:
							showErrorToast("Fehler: Unbekannter Fehler")
							break
					}
					return Promise.reject('Trainer login failed with status ' + response.status)
				}
				return response.json()
			})
			.then(data => {
				useTrainerStore().token = data.token
				setModule(Modules.TRAINER)
			})
			.catch(_ => {
				// Do nothing here, just catch the error to prevent unhandled Promise rejection as it is already handled above in the switch case
			})
	}
</script>

<template>
	<div id="main">
		<div id="form">
			<h1>Trainer-Login</h1>
			<input id="trainer-login-username" v-model="usernameInput" placeholder="Nutzername">
			<input id="trainer-login-password" v-model="passwordInput" type="password" placeholder="Passwort">
			<button id="trainer-login" @click="submit()">
				Übung erstellen
			</button>
		</div>
	</div>
</template>

<style scoped>
	@import url(../../assets/login.css)
</style>