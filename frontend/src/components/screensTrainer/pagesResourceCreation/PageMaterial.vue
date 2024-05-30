<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import socketTrainer from '@/sockets/SocketTrainer'
	import AddMaterialPopup from '@/components/widgets/AddMaterialPopup.vue'
	import {CustomList, ListItem, ListItemButton, ListItemName, ListItemAddButton, ListItemRight} from "@/components/widgets/List"
	import BinButton from '@/components/widgets/BinButton.vue'

	const props = defineProps({
		currentArea: {
			type: Number,
			default: Number.NEGATIVE_INFINITY
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const currentMaterialName = ref('No Material Name')
	const currentMaterialType = ref('No Material Type')
	const currentMaterialId = ref(Number.NEGATIVE_INFINITY)

	const showDeletePopup = ref(false)
	const showAddPopup = ref(false)

	function openDeletePopup(materialName: string, materialId: number) {
		currentMaterialName.value = materialName
		currentMaterialId.value = materialId
		showDeletePopup.value = true
	}

	function openAddPopup(materialType: string) {
		currentMaterialType.value = materialType
		showAddPopup.value = true
	}

	function deleteMaterial() {
		socketTrainer.materialDelete(currentMaterialId.value)
	}

	const devices = computed(() => {
		return currentAreaData.value?.material.filter(material => material.materialType === 'DE') || []
	})

	const bloodList = computed(() => {
		return currentAreaData.value?.material.filter(material => material.materialType === 'BL') || []
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
	<h1>Material</h1>
	<CustomList>
		<ListItemAddButton v-if="currentAreaData" text="Material hinzufügen" @click="openAddPopup('DE')" />
		<ListItem
			v-for="device in devices"
			:key="device.materialName"
		>
			<ListItemButton>
				<ListItemName :name="device.materialName" />
				<ListItemRight>
					<BinButton @click="openDeletePopup(device.materialName, device.materialId)" />
				</ListItemRight>
			</ListItemButton>
		</ListItem>
	</CustomList>
	<CustomList>
		<ListItemAddButton v-if="currentAreaData" text="Blut hinzufügen" @click="openAddPopup('BL')" />
		<ListItem
			v-for="blood in bloodList"
			:key="blood.materialName"
		>
			<ListItemButton>
				<ListItemName :name="blood.materialName" />
				<ListItemRight>
					<BinButton @click="openDeletePopup(blood.materialName, blood.materialId)" />
				</ListItemRight>
			</ListItemButton>
		</ListItem>
	</CustomList>
</template>