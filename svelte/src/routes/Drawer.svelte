<script lang="ts">
	import { fly, slide, scale } from 'svelte/transition';
	import { bounceOut, cubicIn, cubicInOut, circOut } from 'svelte/easing';

	import { AlignJustify, BookCheck, GraduationCap } from 'lucide-svelte';

	let drawerVisible = false;
	let drawerWidth = 300;
</script>

<section class="app">
	<div
		class="main"
		style="transform: {drawerVisible ? 'perspective(800px) translateZ(-40px)' : 'none'}"
	>
		<div class="header">
			<button class="btn-menu" on:click={() => (drawerVisible = !drawerVisible)}
				><AlignJustify /></button
			>
		</div>
	</div>

	{#if drawerVisible}
		<div class="drawer" transition:fly={{ x: -400, easing: circOut }}>
			<button class="btn-menu open" on:click={() => (drawerVisible = !drawerVisible)}>
				<span></span>
				<span></span>
				<span></span>
			</button>
		</div>
	{/if}
</section>

<style>
	:global(body) {
		color: #333;
		margin: 0;
		box-sizing: border-box;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu,
			Cantarell, 'Helvetica Neue', sans-serif;
	}
	.btn-menu {
		height: 60px;
		width: 60px;
		background: none;
		border: none;
		cursor: pointer;
		outline: none;
		position: absolute;
		top: 0;
		left: 0;
	}
	.btn-menu.open {
		left: auto;
		right: 10px;
	}
	.btn-menu span {
		width: 100%;
		height: 5px;
		display: block;
		background: #fff;
		margin: 4px auto;
		transition: all 0.3s;
		backface-visibility: hidden;
	}
	.btn-menu.open span:nth-child(1) {
		transform: rotate(45deg) translate(5px, 5px);
	}
	.btn-menu.open span:nth-child(2) {
		opacity: 0;
	}
	.btn-menu.open span:nth-child(3) {
		transform: rotate(-45deg) translate(7px, -8px);
	}
	.drawer {
		background: #89dfff;
		position: absolute;
		justify-content: space-between;
		display: flex;
		height: 100vh;
		width: 500px;
		z-index: 5;
		opacity: 1;
		transition: transform 750ms 250ms ease-out;
		overflow: hidden;
	}
</style>
