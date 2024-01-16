<script setup>
  import dummyLogin from '../widgets/DummyLogin.vue'

  const emit = defineEmits(['login'])

</script>

<template>
  <div id="main">
    <dummyLogin valid-username="test" valid-password="test" @login="emit('login')" />
  </div>
</template>
  
<style scoped>
  #main {
    height: 100%;
    width: 100%;
  }
</style>