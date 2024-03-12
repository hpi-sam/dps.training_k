<script setup lang="ts">
	import {defineEmits, defineProps} from 'vue'

	withDefaults(defineProps<{
		buttonText: string
	}>(), {
		buttonText: 'Button Text'
	})

	const emits = defineEmits(['on-pressed'])
	const handleClick = () => emits('on-pressed')
</script>

<template>
	<button class="button-mainAction" @click="handleClick">
		{{ buttonText }}
	</button>
</template>

<style scoped>
	.button-mainAction {
		position: absolute;
		bottom: 0;
		background-color: #FFFFFF;
		border: 1px solid rgb(209, 213, 219);
		border-radius: .5rem;
		box-sizing: border-box;
		display: block;
		width: calc(100% - 2rem);
		color: #111827;
		font-size: 1.25rem;
		line-height: 1.25rem;
		padding: .75rem 1rem;
		margin: 1rem;
		text-align: center;
		box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
		cursor: pointer;
		vertical-align: bottom;
	}
</style>