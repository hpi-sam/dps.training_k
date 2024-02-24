<script setup>
	import socketTrainer from "@/sockets/SocketTrainer";
</script>

<template>
	<div id="main">
		<h1>Übung erstellen</h1>
		<button @click="socketTrainer.exerciseCreate()">
			<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
				<path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z" />
			</svg>
		</button>
	</div>
</template>

<style scoped>
	#main {
		height: 100%;
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
	}

	button {
		margin-top: 5px;
		height: 40px;
		width: 40px;
		border-radius: 10px;
	}
</style>