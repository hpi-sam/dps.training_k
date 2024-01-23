<script setup>
  import ScreenTrainer from './screensLogin/ScreenTrainer.vue'
  import ScreenPatient from './screensLogin/ScreenPatient.vue'

  const emit = defineEmits(['switch'])
</script>

<template>
  <div id="leftSide">
    <ScreenTrainer @login-trainer="emit('switch', 'ModuleTrainer')" />
  </div>
  <div id="rightSide">
    <ScreenPatient @login-patient="emit('switch', 'ModulePatient')" />
  </div>
</template>

<style scoped>
  #leftSide, #rightSide{
    float: left;
    width: 50%;
    height: 100%;
  }
</style>