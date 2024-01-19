<script setup>
  import ScreenTrainer from './screensLogin/ScreenTrainer.vue'
  import ScreenPatient from './screensLogin/ScreenPatient.vue'

  const emit = defineEmits(['switch'])
</script>

<template>
  <div id="leftSide">
    <ScreenTrainer @login="emit('switch', 'ModuleTrainer')" />
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
  }
  #rightSide{
    background-color: red;
  }
</style>