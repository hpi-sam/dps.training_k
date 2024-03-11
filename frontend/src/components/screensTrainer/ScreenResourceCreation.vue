<script setup lang="ts">
	import {useExerciseStore} from '@/stores/Exercise'

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(currentArea.value))
</script>
<script lang="ts">
	import {computed, ref} from 'vue'
	
	const currentArea = ref("")

	export const setArea = (newArea: string) => {
		currentArea.value = newArea
	}
</script>
<template>
	<h1>ResourceCreation</h1>
	{{ currentAreaData }}
</template>