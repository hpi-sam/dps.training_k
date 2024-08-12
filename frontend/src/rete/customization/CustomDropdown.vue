<script>
  export default {
    props: ['data']
  }
</script>

<template>
  <div id="dropdown">
    <select v-model="data.value">
      <option v-for="option in data.list" :value="option.value">{{option}}</option>
    </select>
  </div>
</template>

<style scoped>
  #dropdown > select {
    width: 100%;
  }
</style>