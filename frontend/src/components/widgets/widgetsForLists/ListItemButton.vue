<template>
	<button class="list-item-button">
		<slot />
	</button>
</template>

<style>
	.list-item-button {
		position: relative;
		display: flex;
		justify-content: space-between;
		align-items: center;
		height: 50px;
		width: 100%;
		flex-grow: 1;
		flex-wrap: nowrap;
		padding: 0;

		text-align: left;
		background-color: white;
		border: none;
		font-size: 1.25rem;
	}

	.selected .list-item-button {
		filter: brightness(90%);
	}
</style>