<template>
	<div class="list-item">
		<slot />
	</div>
</template>

<style>
	.list-item {
		position: relative;
		border: 1px solid rgb(209, 213, 219);
		display: flex;
		align-items: center;
		text-align: left;
		margin-top: -1px;
		overflow: hidden;
		text-overflow: ellipsis;
		width: 100%;
		font-size: 1.25rem;
		min-height: 50px;
		box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.1);
	}
</style>