<script setup>
  import { ref } from 'vue'

  const props = defineProps({
    validUsername: {
      type: String,
      default: 'abc'
    },
    validPassword: {
      type: String,
      default: '123'
    }
  })
  const emit = defineEmits(['login'])

  const username = ref('')
  const password = ref('')
  const errorOccured = ref(false)
  const errorMassage = ref('')
  

  function submit(){
    if (username.value == props.validUsername && password.value == props.validPassword){
      emit('login')
      errorOccured.value = false
    } else if(username.value == props.validUsername) {
      errorOccured.value = true
      errorMassage.value = "Fehler: falsches Passwort"
    } else {
      errorOccured.value = true
      errorMassage.value = "Fehler: dieser Nutzername existiert nicht"
    }
  }
</script>

<template>
  <div id="main">
    <div id="form">
      <h1>Trainer-Login</h1>
      <input v-model="username" type="text" placeholder="Nutzername">
      <input v-model="password" type="password" placeholder="Passwort">
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