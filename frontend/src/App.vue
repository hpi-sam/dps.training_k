<script setup>
import {computed, ref} from 'vue'
import ModuleLogin from '@/components/ModuleLogin.vue'
import ModuleTrainer from '@/components/ModuleTrainer.vue'
import ModulePatient from '@/components/ModulePatient.vue'
import {state} from "@/socket.js";

const modules = {
  ModuleLogin,
  ModuleTrainer,
  ModulePatient
}

const currentModule = ref('ModulePatient')

const connectionState = computed(() => state.connected)
</script>

<template>
  <main>
    <component :is="modules[currentModule]" />
  </main>
  <div id="dev-bar">
    <button @click="currentModule='ModuleLogin'">
      Login
    </button>
    <button @click="currentModule='ModuleTrainer'">
      Trainer
    </button>
    <button @click="currentModule='ModulePatient'">
      Patient
    </button>
  </div>
  <p>State: {{ connectionState }}</p>
</template>
