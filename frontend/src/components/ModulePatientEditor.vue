<script lang="ts">
import { defineComponent } from 'vue'
import { createEditor as createPatientEditor } from '@/rete/patient'

export default defineComponent({
  async mounted() {
    await createPatientEditor(this.$refs.rete as HTMLElement)
  }
})
</script>

<template>
	<main ref="rete" class="rete" />
</template>

<style scoped>
.rete {
  position: relative;
  height: 100vh;
  font-size: 1rem;
  background: white;
  text-align: left;
  line-height: 1;
}
</style>
