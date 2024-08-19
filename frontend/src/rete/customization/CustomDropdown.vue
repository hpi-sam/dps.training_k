<script lang="ts">
  export default {
    props: ['data']
  }
</script>

<template>
	<div id="dropdown">
		<select v-model="data.selection">
			<option v-for="option in data.optionsList" :key="option" :value="option">
				{{ option.name }}
			</option>
		</select>
	</div>
</template>

<style scoped>
  #dropdown > select {
    width: 100%;
  }
</style>