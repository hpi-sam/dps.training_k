<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"
	import {useAvailablesStore} from "@/stores/Availables"
	import {computed, ref} from "vue"
	import CloseButton from "./CloseButton.vue"
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemRight, ListItemLeft} from "@/components/widgets/List"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		materialType: {
			type: String,
			default: 'Kein Materialtyp ausgewählt'
		},
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const title = computed(() => {
		switch (props.materialType) {
			case 'DE':
				return 'Gerät hinzufügen'
			case 'BL':
				return 'Blut hinzufügen'
			default:
				return 'Kein Materialtyp ausgewählt'
		}
	})

	const availablesStore = useAvailablesStore()
	const availableMaterials = ref(availablesStore.material)

	const availableMaterial = computed(() => {
		return availableMaterials.value.filter(availableMaterial => availableMaterial.materialType === props.materialType)
	})

	function addMaterial(materialName: string){
		socketTrainer.materialAdd(props.currentArea, materialName)
		emit('close-popup')
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup" @click.stop="">
			<CloseButton @close="emit('close-popup')" />
			<div class="scroll">
				<h2>{{ title }}</h2>
				<CustomList>
					<ListItem
						v-for="material in availableMaterial"
						:key="material.materialName"
					>
						<ListItemButton @click="addMaterial(material.materialName)">
							<ListItemName :name="material.materialName" />
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