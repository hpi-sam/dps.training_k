<script setup>
  import LoginPatient from '../widgets/LoginPatient.vue'

  const emit = defineEmits(['loginPatient'])

</script>

<template>
  <div id="main">
    <LoginPatient @login="emit('loginPatient')" />
  </div>
</template>
  
<style scoped>
  #main {
    height: 100%;
    width: 100%;
  }
</style>