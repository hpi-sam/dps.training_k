<script setup lang="ts">
	import CloseButton from "./CloseButton.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		actions: {
			type: Array,
			default: () => [] as string[]
		}
	})
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<div class="scroll">
				<h2>{{ "Ordne eine dieser Aktionen an" }}</h2>
				<div class="list">
					<div
						v-for="(action, index) in props.actions"
						:key="index"
						class="listItem"
					>
						<div class="listItemButton">
							<div class="listItemName">
								{{ action }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<style scoped>
	.popup {
		position: relative;
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		height: 50vh;
		width: 50vw;
	}
</style>