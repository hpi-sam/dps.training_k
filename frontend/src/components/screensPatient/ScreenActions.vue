<script setup lang="ts">
	import PageActionOverview from './pagesAction/PageActionOverview.vue'
	import PageResources from './pagesAction/PageResources.vue'
	import PageActionSelection from './pagesAction/PageActionSelection.vue'
	import {computed, ref} from 'vue'

	enum Pages {
		ACTION_OVERVIEW = "PageActionOverview",
		RESOURCES = "PageResources",
		ACTION_SELECTION = "PageActionSelection",
	}

	const currentPage = ref(Pages.ACTION_OVERVIEW)
	const currentPageComponent = computed(() => getPageComponent(currentPage.value))

	const getPageComponent = (page: Pages) => {
		switch (page) {
			case Pages.ACTION_OVERVIEW:
				return PageActionOverview
			case Pages.RESOURCES:
				return PageResources
			case Pages.ACTION_SELECTION:
				return PageActionSelection
		}
	}

	const setPage = (newPage: Pages) => {
		currentPage.value = newPage
	}
</script>

<template>
	<component :is="currentPageComponent" />
	<nav>
		<button id="nav-action-overview" :class="{ 'selected': currentPage === Pages.ACTION_OVERVIEW }" @click="setPage(Pages.ACTION_OVERVIEW)">
			Übersicht
		</button>
		<button id="nav-resources" :class="{ 'selected': currentPage === Pages.RESOURCES }" @click="setPage(Pages.RESOURCES)">
			Ressourcen
		</button>
		<button id="nav-action-selection" :class="{ 'selected': currentPage === Pages.ACTION_SELECTION }" @click="setPage(Pages.ACTION_SELECTION)">
			Neue Aktion
		</button>
	</nav>
</template>

<style scoped>
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