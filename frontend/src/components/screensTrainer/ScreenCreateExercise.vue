<script setup>
  import {ref} from 'vue'
  import {socket} from "@/socket.js";
  const emit = defineEmits(['switchLeftSide', 'switchRightSide'])
  const errorOccured = ref(false)
  const errorMassage = ref('')
  
  function submit(){
    socket.emit('test-event', JSON.stringify('trainer-exercise-create'))
  }

  socket.on("trainer-exercise-create", (arg) => {
    /** @type {Exercise} */
    const exercise = JSON.parse(arg);
    if(exercise){
        emit('switchRightSide', 'ScreenAreaCreation')
        emit('switchLeftSide', 'ScreenExerciseCreation')
      errorOccured.value = false
    } else {
      errorOccured.value = true
      errorMassage.value = "Fehler: Übung konnte nicht erstellt werden"
    }
    });

</script>
<template>
  <div id="main">
    <button @click="submit()">
      Übung erstellen
    </button>
    <p v-if="errorOccured" id="errorMassage">
      {{ errorMassage }}
    </p>
  </div>
</template>
  
<style scoped>
  #main {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  button{
    border: 2px solid black;
    border-radius: 10px;
    padding: 5px;
    margin: 5px;
    font-size: 1.5em;
  }
  #errorMassage{
    color: red;
  }
</style>