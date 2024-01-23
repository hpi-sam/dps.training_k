<script setup>
  import {ref} from 'vue'
  import {socket} from "@/socket.js";

  const emit = defineEmits(['login'])

  const exerciseCodeInput = ref("")
  const patientCodeInput = ref("")
  const errorOccured = ref(false)
  const errorMassage = ref('')
  

  function submit(){
    socket.emit('patient.login', JSON.stringify({exerciseCode: exerciseCodeInput.value, patientCode: patientCodeInput.value}))
  }

  socket.on("patient.login.response", (arg) => {
    /** @type {boolean} */
    const bool = JSON.parse(arg);
    if(bool){

      emit('login')
      errorOccured.value = false
    } else {
      errorOccured.value = true
      errorMassage.value = "Fehler: Übung oder Patient existiert nicht"
    }
  });

</script>

<template>
  <div id="main">
    <div id="form">
      <h1>Patient-Login</h1>
      <input v-model="exerciseCodeInput" placeholder="Übungscode">
      <input v-model="patientCodeInput" placeholder="Patientencode">
      <input type="submit" value="Login" @click="submit()">
      <p v-if="errorOccured" id="errorMassage">
        {{ errorMassage }}
      </p>
    </div>
  </div>
</template>
  
<style scoped>
  #main {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  #form{
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  input{
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