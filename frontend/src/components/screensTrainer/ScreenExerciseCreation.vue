<script setup>
  import {ref} from 'vue'
  //TODO: load from store
  const trainer = ref('Trainer XY')
  const exerciseCode = ref('Übungscode')
</script>

<template>
  <table>
    <tr>
      <th>
        {{ trainer }}
      </th>
      <th>
        {{ exerciseCode }}
      </th>
    </tr>
  </table>
</template>
    
<style scoped>
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