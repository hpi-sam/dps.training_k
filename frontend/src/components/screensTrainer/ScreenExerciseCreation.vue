<script setup>
  import { useExerciseStore } from '@/stores/Exercise';
  const exerciseStore = useExerciseStore()
</script>

<template>
  <nav>
    <div id="nav-trainer">{{ exerciseStore.getPatient('123').patientCode }}</div>
    <div id="nav-exercise-code">{{ exerciseStore.getExerciseCode }}</div>
  </nav>
  <div>{{ exerciseStore }}</div>
</template>
    
<style scoped>
  nav{
    width: 100%;
    height: 60px;
    display: flex;
    float: left;
  }

  #nav-trainer, #nav-exercise-code{
    width: 50%;
    height: 100%;
    border-bottom: 8px solid black;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5em;
  }

  #nav-trainer{
    border-right: 4px solid black;
  }

  #nav-exercise-code{
    border-left: 4px solid black;
  }
</style>