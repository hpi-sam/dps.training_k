<script setup>
  import {ref} from 'vue'
  import ScreenCreateExercise from './screensTrainer/ScreenCreateExercise.vue'
  import ScreenJoinExercise from './screensTrainer/ScreenJoinExercise.vue'
  import ScreenExerciseCreation from './screensTrainer/ScreenExerciseCreation.vue'
  import ScreenAreaCreation from './screensTrainer/ScreenAreaCreation.vue'

  const screens = {
    ScreenCreateExercise,
    ScreenJoinExercise,
    ScreenExerciseCreation,
    ScreenAreaCreation
  }

  const currentLeftSide = ref('ScreenCreateExercise')
  const currentRightSide = ref('ScreenJoinExercise')
</script>

<template>
  <div id="leftSide">
    <component :is="screens[currentLeftSide]" @switch-left-side="(to) => currentLeftSide = to" @switch-right-side="(to) => currentRightSide = to" />
  </div>
  <div id="rightSide">
    <component :is="screens[currentRightSide]" @switch-left-side="(to) => currentLeftSide = to" @switch-right-side="(to) => currentRightSide = to" />
  </div>
</template>

<style scoped>
  #leftSide, #rightSide{
    float: left;
    width: 50%;
    height: 100%;
  }
</style>