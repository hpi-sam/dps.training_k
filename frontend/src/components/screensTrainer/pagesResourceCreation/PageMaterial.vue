<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import socketTrainer from '@/sockets/SocketTrainer'
	import AddMaterialPopup from '@/components/widgets/AddMaterialPopup.vue'

	const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const currentMaterialName = ref('No Material Name')
	const currentMaterialType = ref('No Material Type')

	const showDeletePopup = ref(false)
	const showAddPopup = ref(false)

	function openDeletePopup(materialName: string) {
		currentMaterialName.value = materialName
		showDeletePopup.value = true
	}

	function openAddPopup(materialType: string) {
		currentMaterialType.value = materialType
		showAddPopup.value = true
	}

	function deleteMaterial() {
		socketTrainer.materialDelete(currentMaterialName.value)
	}

	const devices = computed(() => {
		return currentAreaData.value?.material.filter(material => material.materialType === 'device') || []
	})

	const bloodList = computed(() => {
		return currentAreaData.value?.material.filter(material => material.materialType === 'blood') || []
	})
</script>

<template>
	<DeleteItemPopup
		v-if="showDeletePopup"
		:name="currentMaterialName"
		@delete="deleteMaterial"
		@close-popup="showDeletePopup=false"
	/>
	<AddMaterialPopup
		v-if="showAddPopup"
		:material-type="currentMaterialType"
		:current-area="props.currentArea"
		@close-popup="showAddPopup=false"
	/>
	<div class="scroll">
		<h1>Material</h1>
		<div class="list">
			<button v-if="currentAreaData" class="listItemAddButton" @click="openAddPopup('device')">
				Gerät hinzufügen
			</button>
			<div
				v-for="device in devices as Material[]"
				:key="device.materialName"
				class="listItem"
			>
				<button class="listItemButton" @click="openDeletePopup(device.materialName)">
					<div class="listItemName">
						{{ device.materialName }}
					</div>
				</button>
			</div>
		</div>
		<div class="list">
			<button v-if="currentAreaData" class="listItemAddButton" @click="openAddPopup('blood')">
				Blut hinzufügen
			</button>
			<div
				v-for="blood in bloodList as Material[]"
				:key="blood.materialName"
				class="listItem"
			>
				<button class="listItemButton" @click="openDeletePopup(blood.materialName)">
					<div class="listItemName">
						{{ blood.materialName }}
					</div>
				</button>
			</div>
		</div>
	</div>
</template>