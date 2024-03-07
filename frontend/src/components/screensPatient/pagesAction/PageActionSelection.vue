<script setup lang="ts">
	import socketPatient from '@/sockets/SocketPatient'

	function actionAdd(actionName: string) {
		socketPatient.actionAdd(actionName)
	}
</script>

<template>
	<h1>ActionSelection</h1>
	<button @click="actionAdd('testAction')">Fügt eine Test-Aktion hinzu</button>
</template>