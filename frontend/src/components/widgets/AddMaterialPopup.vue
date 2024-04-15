<script setup lang="ts">
	import socketTrainer from "@/sockets/SocketTrainer"
	import { useAvailablesStore } from "@/stores/Availables"
	import { computed ,ref } from "vue"

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
			case 'device':
				return 'Gerät hinzufügen'
			case 'blood':
				return 'Blut hinzufügen'
			default:
				return 'Kein Materialtyp ausgewählt'
		}
	})

	const availablesStore = useAvailablesStore()
	const availableMaterialList = ref(availablesStore.material)

	const availableMaterial = computed(() => {
		return availableMaterialList.value.filter(availableMaterial => availableMaterial.materialType === props.materialType)
	})

	function addMaterial(materialName: string){
		socketTrainer.materialAdd(props.currentArea, materialName)
		emit('close-popup')
	}
</script>

<template>
	<div class="popup-overlay" @click="emit('close-popup')">
		<div class="popup scroll" @click.stop="">
			<div class="flex-container">
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
		background-color: white;
		padding: 20px;
		border-radius: 8px;
		height: fit-content;
		max-height: 50vh;
	}
</style>