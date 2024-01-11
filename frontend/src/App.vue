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
  <main>
    <component :is="modules[currentModule]"></component>
  </main>
  <div id="dev-bar">
    <button @click="currentModule='ModuleLogin'">Login</button>
    <button @click="currentModule='ModuleTrainer'">Trainer</button>
    <button @click="currentModule='ModulePatient'">Patient</button>
  </div>
</template>
