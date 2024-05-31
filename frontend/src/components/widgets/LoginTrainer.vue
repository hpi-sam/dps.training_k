<script setup lang="ts">
	import {ref} from 'vue'
	import {useTrainerStore} from '@/stores/Trainer'
	import socketTrainer from '@/sockets/SocketTrainer'

	const usernameInput = ref("")
	const passwordInput = ref("")

	function submit() {
		const trainerStore = useTrainerStore()
		trainerStore.username = usernameInput.value
		socketTrainer.connect()
		return
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