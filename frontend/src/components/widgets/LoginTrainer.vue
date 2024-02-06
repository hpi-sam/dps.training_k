<script setup>
  import {ref} from 'vue'
  import {trainerLogin} from "@/socket.js";

  const usernameInput = ref("")
  const passwordInput = ref("")

  function submit(){
    trainerLogin(usernameInput.value, passwordInput.value)
  }
</script>

<template>
  <div id="main">
    <div id="form">
      <h1>Trainer-Login</h1>
      <input v-model="usernameInput" placeholder="Nutzername">
      <input v-model="passwordInput" type="password" placeholder="Passwort">
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