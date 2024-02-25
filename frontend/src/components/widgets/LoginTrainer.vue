<script setup lang="ts">
	import {ref} from 'vue'
	import {useTrainerStore} from '@/stores/Trainer';
	import {Modules, setModule, showErrorToast} from "@/App.vue";

	const usernameInput = ref("")
	const passwordInput = ref("")

	function submit() {
		const trainerStore = useTrainerStore()
		trainerStore.username = usernameInput.value

		const requestBody = {
			"messageType": "trainer-login",
			"username": usernameInput.value,
			"password": passwordInput.value,
		}

		fetch('https://localhost:8000/login/', {
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
					return Promise.reject('Trainer login failed with status ' + response.status);
				}
				return response.json();
			})
			.then(data => {
				trainerStore.token = data.token
				setModule(Modules.TRAINER)
			})
	}
</script>

<template>
	<div id="main">
		<div id="form">
			<h1>Trainer-Login</h1>
			<input v-model="usernameInput" placeholder="Nutzername">
			<input v-model="passwordInput" type="password" placeholder="Passwort">
			<button @click="submit()">
				<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
					<!-- eslint-disable-next-line max-len, vue/max-len -->
					<path d="M480-120v-80h280v-560H480v-80h280q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H480Zm-80-160-55-58 102-102H120v-80h327L345-622l55-58 200 200-200 200Z" />
				</svg>
			</button>
		</div>
	</div>
</template>

<style scoped>
	@import url(../../assets/login.css);
</style>