<template>
	<div class="list-item-left">
		<slot />
	</div>
</template>

<style>
    .list-item-left {
		margin-left: 16px;
        display: flex;
        justify-content: center;
        flex-shrink: 0;
	}
</style>