<script setup>
import { ref } from 'vue'
import ModuleLogin from '@/components/ModuleLogin.vue'
import ModuleTrainer from '@/components/ModuleTrainer.vue'
import ModulePatient from '@/components/ModulePatient.vue'

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
