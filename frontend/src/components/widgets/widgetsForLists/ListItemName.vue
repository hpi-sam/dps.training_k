<script setup lang="ts">
    const props = defineProps({
		name: {
			type: String,
			default: "Fehlende Bezeichnung"
		}
	})
</script>

<template>
	<div class="list-item-name">
		{{ props.name }}
	</div>
</template>

<style>
    .list-item-name {
        padding: .75rem 1rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        flex: 1;
        width: 100%;
    }
</style>