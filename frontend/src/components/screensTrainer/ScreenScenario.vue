<script setup lang="ts">
	import ExerciseControlPanel from "../widgets/ExerciseControlPanel.vue"
	import TopBarTrainer from "@/components/widgets/TopBarTrainer.vue"
</script>

<template>
	<div class="flex-container">
		<TopBarTrainer />
		<div class="scroll">
			<h1>Scenario Screen</h1>
		</div>
		<ExerciseControlPanel />
	</div>
</template>

<style scoped>
	.scroll {
		margin-bottom: 50px;
	}
</style>