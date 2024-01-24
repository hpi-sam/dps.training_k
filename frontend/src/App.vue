<script setup>
import {computed, ref} from 'vue'
import ModuleLogin from '@/components/ModuleLogin.vue'
import ModuleTrainer from '@/components/ModuleTrainer.vue'
import ModulePatient from '@/components/ModulePatient.vue'
import {serverEvents, socket, state} from "@/socket.js";

const modules = {
  ModuleLogin,
  ModuleTrainer,
  ModulePatient
}

const currentModule = ref('ModuleLogin')

const connectionState = computed(() => state.connected ? "connected" : "disconnected")
</script>


<template>
  <main>
    <component :is="modules[currentModule]" @switch="(to) => currentModule = to" />
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

    <button id="ws-test" @click="socket.emit('test-passthrough')">
      send pass-through test
    </button>

    <!-- change the stringified event to test different server-side events -->
    <button id="ws-test" @click="socket.emit('test-event', JSON.stringify(serverEvents.patientLoadRunning))">
      send event test
    </button>

    <p id="ws-test">
      Backend-Proxy: {{ connectionState }}
    </p>
  </div>
</template>


<style scoped>
#dev-bar {
  display: flex;
  align-items: center;
}

#ws-test {
  margin-left: 20px;
}
</style>