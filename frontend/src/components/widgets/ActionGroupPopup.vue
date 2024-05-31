<script setup lang="ts">
	import CloseButton from "./CloseButton.vue"
	import {CustomList, ListItem, ListItemButton, ListItemName} from "@/components/widgets/List"

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
				<CustomList>
					<ListItem
						v-for="(action, index) in props.actions"
						:key="index"
					>
						<ListItemButton>
							<ListItemName :name="action as string" />
						</ListItemButton>
					</ListItem>
				</CustomList>
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