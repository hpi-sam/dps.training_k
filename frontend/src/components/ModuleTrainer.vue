<script>
  import {ref} from 'vue'
  const currentLeftScreen = ref('ScreenCreateExercise')
  const currentRightScreen = ref('ScreenJoinExercise')

  export function setLeftScreen(newScreen) {
    currentLeftScreen.value = newScreen
  }
  export function setRightScreen(newScreen) {
    currentRightScreen.value = newScreen
  }
</script>

<script setup>
  import ScreenCreateExercise from './screensTrainer/ScreenCreateExercise.vue'
  import ScreenJoinExercise from './screensTrainer/ScreenJoinExercise.vue'
  import ScreenExerciseCreation from './screensTrainer/ScreenExerciseCreation.vue'
  import ScreenResourceCreation from './screensTrainer/ScreenResourceCreation.vue'

  const screens = {
    ScreenCreateExercise,
    ScreenJoinExercise,
    ScreenExerciseCreation,
    ScreenResourceCreation
  }
</script>

<template>
  <div id="leftScreen">
    <component :is="screens[currentLeftScreen]" />
  </div>
  <div id="rightScreen">
    <component :is="screens[currentRightScreen]" />
  </div>
</template>

<style scoped>
  #leftScreen, #rightScreen{
    float: left;
    width: 50%;
    height: 100%;
    border: 8px solid black;
  }
  #leftScreen{
    border-right: 4px solid black;
  }
  #rightScreen{
    border-left: 4px solid black;
  }
</style>