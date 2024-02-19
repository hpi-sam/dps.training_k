<script setup>
	import {onBeforeUnmount, onMounted} from 'vue'
	import socketPatient from "@/sockets/SocketPatient.js";
	import {connectionStore} from "@/sockets/ConnectionStore.js";

	onMounted(() => socketPatient.connect());
	onBeforeUnmount(() => {
		if (connectionStore.patientConnected) socketPatient.close();
	});
</script>

<template>
	<h1>Patient</h1>
</template>