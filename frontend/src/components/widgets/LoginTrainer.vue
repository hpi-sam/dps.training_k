<script setup>
  import {ref} from 'vue'
  import {socket} from "@/socket.js";

  const emit = defineEmits(['login'])

  const usernameInput = ref("")
  const passwordInput = ref("")
  const errorOccured = ref(false)
  const errorMassage = ref('')
  

  function submit(){
    socket.emit('trainer.login', JSON.stringify({username: usernameInput.value, password: passwordInput.value}))
  }

  socket.on("trainer.login.response", (arg) => {
    /** @type {boolean} */
    const bool = JSON.parse(arg);
    if(bool){
      emit('login')
      errorOccured.value = false
    } else {
      errorOccured.value = true
      errorMassage.value = "Fehler: falscher Nutzername oder falsches Passwort"
    }
  });

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