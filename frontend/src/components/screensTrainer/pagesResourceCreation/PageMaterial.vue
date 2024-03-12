<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'

    const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))
</script>

<template>
	<h1>Patienten</h1>
	{{ currentAreaData?.devices }}
</template>

<style scoped>
</style>