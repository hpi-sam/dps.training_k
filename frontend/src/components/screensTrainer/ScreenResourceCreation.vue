<script setup lang="ts">
	import PagePatients from './pagesResourceCreation/PagePatients.vue'
	import PagePersonnel from './pagesResourceCreation/PagePersonnel.vue'
	import PageMaterial from './pagesResourceCreation/PageMaterial.vue'
	import {computed, ref} from 'vue'

	enum Pages {
		PATIENTS = "PagePatients",
		PERSONNEL = "PagePersonnel",
		MATERIAL = "PageMaterial",
	}

	const currentPage = ref(Pages.PATIENTS)
	const currentPageComponent = computed(() => getPageComponent(currentPage.value))

	const getPageComponent = (page: Pages) => {
		switch (page) {
			case Pages.PATIENTS:
				return PagePatients
			case Pages.PERSONNEL:
				return PagePersonnel
			case Pages.MATERIAL:
				return PageMaterial
		}
	}

	const setPage = (newPage: Pages) => {
		currentPage.value = newPage
	}
</script>

<script lang="ts">
	const currentArea = ref("")

	export const setArea = (newArea: string) => {
		currentArea.value = newArea
	}
</script>

<template>
	<p v-if="!currentArea" id="noAreaText">
		Wähle einen Bereich aus
	</p>
	<component :is="currentPageComponent" :current-area="currentArea" />
	<nav>
		<button id="nav-patients" :class="{ 'selected': currentPage === Pages.PATIENTS }" @click="setPage(Pages.PATIENTS)">
			Patienten
		</button>
		<button id="nav-personnel" :class="{ 'selected': currentPage === Pages.PERSONNEL }" @click="setPage(Pages.PERSONNEL)">
			Personal
		</button>
		<button id="nav-material" :class="{ 'selected': currentPage === Pages.MATERIAL }" @click="setPage(Pages.MATERIAL)">
			Material
		</button>
	</nav>
</template>

<style scoped>
	#noAreaText {
		text-align: center;
		font-size: 1.8em;
		margin-top: 40px;
	}

	nav {
		width: 100%;
		height: 60px;
		bottom: 0;
		position: absolute;
		display: flex;
		float: left;
	}

	button {
		width: calc(100% / 3);
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.5em;
		background-color: lightgray;
		border: none;
		border-top: 8px solid black;
	}

	button.selected {
		background-color: white;
		font-weight: bold;
	}

	#nav-patients {
		border-right: 4px solid black;
	}

	#nav-personnel {
		border-left: 4px solid black;
		border-right: 4px solid black;
	}

	#nav-material {
		border-left: 4px solid black;
	}
</style>