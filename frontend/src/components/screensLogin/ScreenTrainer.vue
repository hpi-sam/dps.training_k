<script setup>
  import LoginTrainer from '../widgets/LoginTrainer.vue'

  const emit = defineEmits(['loginTrainer'])

</script>

<template>
  <div id="main">
    <LoginTrainer @login="emit('loginTrainer')" />
  </div>
</template>
  
<style scoped>
  #main {
    height: 100%;
    width: 100%;
  }
</style>