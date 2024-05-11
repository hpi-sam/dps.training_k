<script setup lang="ts">
	import socketTrainer, {serverMockEvents as serverMockEventsTrainer} from "@/sockets/SocketTrainer"

	async function startDemo() {
		socketTrainer.socket.onmessage({data: serverMockEventsTrainer.find(e => e.id === 'exercise').data} as MessageEvent)
		socketTrainer.socket.onmessage({data: serverMockEventsTrainer.find(e => e.id === 'available-material').data} as MessageEvent)
		socketTrainer.socket.onmessage({data: serverMockEventsTrainer.find(e => e.id === 'log-update-1').data} as MessageEvent)
		socketTrainer.socket.onmessage({data: serverMockEventsTrainer.find(e => e.id === 'log-update-2').data} as MessageEvent)
	}
</script>

<template>
	<div id="main">
		<button
			id="button"
			:style="{backgroundColor: 'var(--yellow)', color: 'white'}"
			@click="startDemo"
		>
			Demo starten
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
	#button {
		position: relative;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		width: 180px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: center;
		margin-top: 10px;
	}
</style>