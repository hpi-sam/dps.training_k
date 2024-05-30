<script setup lang="ts">
    import {svg} from "@/assets/Svg"
</script>

<template>
	<button class="bin-button">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			height="24"
			viewBox="0 -960 960 960"
			width="24"
		>
			<path :d="svg.binIcon" />
		</svg>
	</button>
</template>

<style>
	.bin-button {
		height: 50px;
		width: 50px;
		border: none;
		background-color: white;
		margin-left: auto;
	}

    .bin-button:hover {
        filter: none;
    }
</style>