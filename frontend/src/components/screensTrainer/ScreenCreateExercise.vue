<template>
	<div id="main">
		<h1>Übung erstellen</h1>
		<button @click="trainerExerciseCreate()">
			<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
				<path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z" />
			</svg>
		</button>
	</div>
</template>

<script setup>
	import {trainerExerciseCreate} from "@/socket.js";
</script>

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