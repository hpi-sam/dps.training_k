<script setup lang="ts">
	import PageActionOverview from './pagesAction/PageActionOverview.vue'
	import PageActionSelection from './pagesAction/PageActionSelection.vue'
	import PagePersonnel from './pagesAction/PagePersonnel.vue'
	import PageMaterial from './pagesAction/PageMaterial.vue'
	import {computed, ref} from 'vue'

	enum Pages {
		ACTION_OVERVIEW = "PageActionOverview",
		ACTION_SELECTION = "PageActionSelection",
		PERSONNEL = "PagePersonnel",
		MATERIAL = "PageMaterial"
	}

	const currentPage = ref(Pages.ACTION_OVERVIEW)
	const currentPageComponent = computed(() => getPageComponent(currentPage.value))

	const getPageComponent = (page: Pages) => {
		switch (page) {
			case Pages.ACTION_OVERVIEW:
				return PageActionOverview
			case Pages.ACTION_SELECTION:
				return PageActionSelection
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

<template>
	<div class="page">
		<component
			:is="currentPageComponent"
			@add-action="setPage(Pages.ACTION_SELECTION)"
			@close-action-selection="setPage(Pages.ACTION_OVERVIEW)"
		/>
	</div>
	<nav>
		<button
			id="nav-left"
			:class="{ 'selected': currentPage === Pages.ACTION_OVERVIEW }"
			@click="setPage(Pages.ACTION_OVERVIEW)"
		>
			Übersicht
		</button>
		<button id="nav-center" :class="{ 'selected': currentPage === Pages.PERSONNEL }" @click="setPage(Pages.PERSONNEL)">
			Personal
		</button>
		<button id="nav-right" :class="{ 'selected': currentPage === Pages.MATERIAL }" @click="setPage(Pages.MATERIAL)">
			Material
		</button>
	</nav>
</template>

<style scoped>
	.page {
		height: calc(100% - 60px);
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

	#nav-left {
		border-right: 4px solid black;
	}

	#nav-center {
		border-left: 4px solid black;
		border-right: 4px solid black;
	}

	#nav-right {
		border-left: 4px solid black;
	}
</style>