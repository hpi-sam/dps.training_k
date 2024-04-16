<script setup lang="ts">
	const emit = defineEmits(['add-action'])
</script>

<template>
	<h1>Übersicht</h1>
	<div class="scroll">
		<div class="list">
			<button class="listItemAddButton" @click="emit('add-action')">
				Aktion hinzufügen
			</button>
		</div>
	</div>
</template>