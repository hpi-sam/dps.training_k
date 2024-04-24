<script setup lang="ts">
    import { svg } from '@/assets/Svg'

    const emit = defineEmits(['close'])
</script>

<template>
	<button class="close-button" @click="emit('close')">
		<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
			<path :d="svg.closeIcon" />
		</svg>
	</button>
</template>

<style scoped>
	.close-button {
		position: absolute;
		display: flex;
		justify-content: center;
		align-items: center;
		margin-left: auto;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		top: 1rem;
		right: 1rem;
		width: 2.5rem;
		height: 2.5rem;
		font-size: 1.25rem;
		line-height: 1.25rem;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
		flex-grow: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		z-index: 1;
	}
</style>