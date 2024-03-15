<script setup lang="ts">
	const props = defineProps({
		isChecked: {
			type: Boolean,
			default: true
		}
	})
</script>

<template>
	<div class="toggleSwitch">
		<label>
			<input type="checkbox" :checked="props.isChecked">
			<span class="slider" />
		</label>
	</div>
</template>

<style scoped>
.toggleSwitch {
	position: relative;
	display: inline-block;
	width: 80px;
	height: 24px;
}

.toggleSwitch input { 
	opacity: 0;
	width: 0;
	height: 0;
}

.slider {
	position: absolute;
	cursor: pointer;
	top: 0;
	left: 10px;
	right: 10px;
	bottom: 0;
	background-color: #ccc;
	transition: .1s;
	border-radius: 34px;
	margin-right: 5px;
}

.slider:before {
	position: absolute;
	content: "";
	height: 20px;
	width: 20px;
	left: 2px;
	right: 10px;
	bottom: 2px;
	background-color: white;
	transition: .1s;
	border-radius: 50%;
}

input:checked + .slider {
	background-color: #2196F3;
}

input:checked + .slider:before {
	transform: translateX(22px);
}
</style>