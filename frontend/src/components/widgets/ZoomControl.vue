<template>
	<div class="zoom-control">
		<button @click="zoomIn">
			+
		</button>
		<button @click="zoomOut">
			-
		</button>
		<button @click="resetZoom">
			Reset
		</button>
	</div>
</template>
  
  <script setup lang="ts">
  import { defineComponent, inject } from 'vue'
  
  const zoomPlugin = inject('zoomPlugin')
  
  const zoomIn = () => {
    zoomPlugin?.wheel({ deltaY: -1 } as WheelEvent)
  }
  
  const zoomOut = () => {
    zoomPlugin?.wheel({ deltaY: 1 } as WheelEvent)
  }
  
  const resetZoom = () => {
    zoomPlugin?.wheel({ deltaY: 0 } as WheelEvent) // Customize this based on actual reset logic
  }
  </script>
  
  <style scoped>
  .zoom-control {
    position: absolute;
    top: 20px;
    right: 20px;
    display: flex;
    flex-direction: column;
  }
  
  .zoom-control button {
    margin: 5px 0;
    padding: 10px;
    border: none;
    background-color: var(--green);
    color: white;
    font-size: 16px;
    cursor: pointer;
  }
  
  .zoom-control button:hover {
    background-color: var(--dark-green);
  }
  </style>
  