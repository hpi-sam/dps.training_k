<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {useExerciseStore} from '@/stores/Exercise'
	import ToggleSwitchForListItems from '@/components/widgets/ToggleSwitchForListItems.vue'
	import DeleteItemPopup from '@/components/widgets/DeleteItemPopup.vue'
	import socketTrainer from '@/sockets/SocketTrainer'

    const props = defineProps({
		currentArea: {
			type: String,
			default: "Kein Bereich ausgewählt"
		}
	})

	const exerciseStore = useExerciseStore()

	const currentAreaData = computed(() => exerciseStore.getArea(props.currentArea))

	const currentItem = ref('')

	const showPopup = ref(false)

	function openPopup(materialName: string) {
		currentItem.value = materialName
		showPopup.value = true
	}

	function addMaterial() {
		//socketTrainer.materialAdd(props.currentArea)
	}

	function deleteMaterial(){
		socketTrainer.materialDelete(currentItem.value)
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
		v-if="showPopup"
		:name="currentItem"
		@delete="deleteMaterial"
		@close-popup="showPopup=false"
	/>
	<div class="list">
		<div
			v-for="device in devices"
			:key="device.materialName"
			class="listItem"
		>
			<button class="listItemButton" @click="openPopup(device.materialName)">
				<div class="listItemName">
					{{ device.materialName }}
				</div>
			</button>
			<ToggleSwitchForListItems default="active" />
		</div>
		<button v-if="currentAreaData" class="listItemAddButton" @click="addMaterial()">
			Gerät hinzufügen
		</button>
	</div>
	<div class="list">
		<div
			v-for="blood in bloodList"
			:key="blood.materialName"
			class="listItem"
		>
			<button class="listItemButton" @click="openPopup(blood.materialName)">
				<div class="listItemName">
					{{ blood.materialName }}
				</div>
			</button>
			<ToggleSwitchForListItems default="active" />
		</div>
		<button v-if="currentAreaData" class="listItemAddButton" @click="addMaterial()">
			Blut hinzufügen
		</button>
	</div>
</template>