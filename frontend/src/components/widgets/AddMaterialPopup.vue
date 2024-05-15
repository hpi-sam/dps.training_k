<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"
	import {useAvailablesStore} from "@/stores/Availables"
	import {computed, ref} from "vue"
	import CloseButton from "./CloseButton.vue"

	const emit = defineEmits(['close-popup'])

	const props = defineProps({
		materialType: {
			type: String,
			default: 'Kein Materialtyp ausgewählt'
		},
		currentArea: {
			type: String,
			default: 'Kein Bereich ausgewählt'
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
				<div class="list">
					<div
						v-for="material in availableMaterial"
						:key="material.materialName"
						class="listItem"
					>
						<button class="listItemButton" @click="addMaterial(material.materialName)">
							<div class="listItemName">
								{{ material.materialName }}
							</div>
						</button>
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