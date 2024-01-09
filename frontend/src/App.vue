<script setup>
import { ref } from 'vue'
import ModuleLogin from './modules/ModuleLogin.vue'
import ModuleTrainer from './modules/ModuleTrainer.vue'
import ModulePatient from './modules/ModulePatient.vue'

const modules = {
  ModuleLogin,
  ModuleTrainer,
  ModulePatient
}

const currentModule = ref('ModulePatient')
</script>

<template>
  <div id="dev-bar">
    <button @click="currentModule='ModuleLogin'">Login</button>
    <button @click="currentModule='ModuleTrainer'">Trainer</button>
    <button @click="currentModule='ModulePatient'">Patient</button>
  </div>
  <br/>
  <main>
    <component :is="modules[currentModule]"></component>
  </main>
</template>
