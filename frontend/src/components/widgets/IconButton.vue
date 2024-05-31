<script setup lang="ts">
	import {svg} from "@/assets/Svg"

	const props = defineProps({
		icon: {
			type: String,
			default: svg.closeIcon
		}
	})
</script>

<template>
	<button class="icon-button">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			height="24"
			viewBox="0 -960 960 960"
			width="24"
		>
			<path :d="props.icon" />
		</svg>
	</button>
</template>

<style>
	.icon-button {
		height: 50px;
		width: 50px;
		border: none;
		background-color: white;
		margin-left: auto;
	}

    .icon-button:hover {
        filter: none;
    }
</style>