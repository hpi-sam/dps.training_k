<script setup lang="ts">
	import {computed, ref} from 'vue'
	import {usePatientStore} from '@/stores/Patient'

	const patientStore = usePatientStore()
</script>
<script lang="ts">
	import PageActionOverview from './pagesAction/PageActionOverview.vue'
	import PageResources from './pagesAction/PageResources.vue'
	import PageActionSelection from './pagesAction/PageActionSelection.vue'

	export enum Pages {
		ACTIONOVERVIEW = "PageActionOverview",
		RESOURCES = "PageResources",
		ACTIONSELECTION = "PageActionSelection",
	}
	const currentPage = ref(Pages.ACTIONOVERVIEW)
	const currentPageComponent = computed(() => getPageComponent(currentPage.value))

	const getPageComponent = (page: Pages) => {
		switch (page) {
			case Pages.ACTIONOVERVIEW:
				return PageActionOverview
			case Pages.RESOURCES:
				return PageResources
			case Pages.ACTIONSELECTION:
				return PageActionSelection
		}
	}

	export const setPage = (newPage: Pages) => {
		currentPage.value = newPage
	}
</script>

<template>
	<component :is="currentPageComponent" />
	<nav>
		<button id="nav-action-overview" :class="{ 'selected': currentPage === Pages.ACTIONOVERVIEW }" @click="setPage(Pages.ACTIONOVERVIEW)">
			Übersicht
		</button>
		<button id="nav-resources" :class="{ 'selected': currentPage === Pages.RESOURCES }" @click="setPage(Pages.RESOURCES)">
			Ressourcen
		</button>
		<button id="nav-action-selection" :class="{ 'selected': currentPage === Pages.ACTIONSELECTION }" @click="setPage(Pages.ACTIONSELECTION)">
			Neue Aktion
		</button>
	</nav>
</template>

<style scoped>
	nav {
		width: 100%;
		height: 60px;
		bottom: 0px;
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
		background-color: white;
		border: none;
		border-top: 8px solid black;
	}

	button.selected {
		border-top: none;
	}

	#nav-action-overview {
		border-right: 4px solid black;
	}

	#nav-resources {
		border-left: 4px solid black;
		border-right: 4px solid black;
	}

	#nav-action-selection {
		border-left: 4px solid black;
	}
</style>