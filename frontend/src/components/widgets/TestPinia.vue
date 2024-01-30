<script setup>
    import { useExerciseStore } from '@/stores/Exercise'

    function testPinia(){
        const exerciseStore = useExerciseStore()
        console.log(exerciseStore.exerciseCode)
        console.log(exerciseStore.getExerciseCode)
        console.log(exerciseStore.getArea('800'))
        console.log(exerciseStore.getPatient('800'))
    }
</script>
<template>
  <button id="ws-test" @click="testPinia()">
    test pinia
  </button>
</template>