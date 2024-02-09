<script setup>
  import ScreenTrainer from './screensLogin/ScreenTrainer.vue'
  import ScreenPatient from './screensLogin/ScreenPatient.vue'
</script>

<template>
  <div id="leftSide">
    <ScreenTrainer />
  </div>
  <div id="rightSide">
    <ScreenPatient />
  </div>
</template>

<style scoped>
  #leftSide, #rightSide{
    float: left;
    width: 50%;
    height: 100%;
    border: 8px solid black;
  }
  #leftSide{
    border-right: 4px solid black;
  }
  #rightSide{
    border-left: 4px solid black;
  }
</style>