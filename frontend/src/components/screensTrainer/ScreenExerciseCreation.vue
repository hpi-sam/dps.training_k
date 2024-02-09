<script setup>
  import {ref} from 'vue'
  //TODO: load from store
  const trainer = ref('Trainer XY')
  const exerciseCode = ref('Übungscode')
</script>

<template>
  <nav>
    <div id="nav-trainer">{{ trainer }}</div>
    <div id="nav-exercise-code">{{ exerciseCode }}</div>
  </nav>
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
  }

  #nav-trainer{
    border-right: 4px solid black;
  }

  #nav-exercise-code{
    border-left: 4px solid black;
  }

  table, td, th {
    border: 1px solid;
  }

  table{
    width: 100%;
    height: 70px;
    border-collapse: collapse;
  }

  th {
    width: 50%;
    font-size: 20px;
  }
</style>