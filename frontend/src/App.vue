<script setup>
import {computed, ref} from 'vue'
import ModuleLogin from '@/components/ModuleLogin.vue'
import ModuleTrainer from '@/components/ModuleTrainer.vue'
import ModulePatient from '@/components/ModulePatient.vue'
import {socket, state} from "@/socket.js";

const modules = {
  ModuleLogin,
  ModuleTrainer,
  ModulePatient
}

const currentModule = ref('ModulePatient')

const connectionState = computed(() => state.connected ? "connected" : "disconnected")
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
    <button id="test-button" @click="socket.emit('test')">
      send test event
    </button>
    <p>Mock-Backend: {{ connectionState }}</p>
  </div>
</template>


<style scoped>
#dev-bar {
  display: flex;
  align-items: center;
}

#test-button {
  margin-left: 20px;
  margin-right: 10px;
}
</style>