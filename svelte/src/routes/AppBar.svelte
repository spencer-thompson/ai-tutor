<script lang="ts">
	import { AppRail, AppRailTile, AppRailAnchor, AppBar, popup } from '@skeletonlabs/skeleton';
	import type { PopupSettings } from '@skeletonlabs/skeleton';
	import { AlignJustify, BookCheck, GraduationCap } from 'lucide-svelte';
	import { fly, slide, scale } from 'svelte/transition';
	import { bounceOut, cubicIn, cubicInOut, circOut } from 'svelte/easing';

	const popupClick: PopupSettings = {
		event: 'click',
		target: 'popupClick',
		placement: 'bottom',
		closeQuery: '#will-close',
		shift: { crossAxis: false },
		arrow: { padding: 80 }
	};

	let currentTile: number = 0;

	let appRailVisible = false;
</script>

<div class="fixed z-50">
	<AppRail width="w-20" background="bg-transparent">
		<svelte:fragment slot="lead">
			<AppRailAnchor>
				<button
					class="btn-menu open"
					on:click|preventDefault={() => (appRailVisible = !appRailVisible)}
				>
					<div class="flex justify-center items-center w-full">
						<GraduationCap size="56" />
					</div>
				</button>
			</AppRailAnchor>
		</svelte:fragment>
	</AppRail>
</div>

{#if appRailVisible}
	<div class="fixed" transition:fly={{ x: -100, duration: 800 }}>
		<AppRail width="w-20" background="bg-transparent">
			<svelte:fragment slot="lead">
				<AppRailAnchor>
					<button
						class="btn-menu open"
						on:click|preventDefault={() => (appRailVisible = !appRailVisible)}
					>
						<div class="flex justify-center items-center w-full"></div>
					</button>
				</AppRailAnchor>
			</svelte:fragment>
			<AppRailTile bind:group={currentTile} name="tile-1" value={0} title="tile-1">
				<svelte:fragment slot="lead">
					<div class="flex justify-center items-center w-full">
						<BookCheck />
					</div>
				</svelte:fragment>
				<span>Tile 1</span>
			</AppRailTile>
			<AppRailTile bind:group={currentTile} name="tile-2" value={1} title="tile-2">
				<svelte:fragment slot="lead"></svelte:fragment>
				<span>Tile 2</span>
			</AppRailTile>
			<AppRailTile bind:group={currentTile} name="tile-3" value={2} title="tile-3">
				<svelte:fragment slot="lead">(icon)</svelte:fragment>
				<span>Tile 3</span>
			</AppRailTile>
			<!-- --- -->
			<svelte:fragment slot="trail">
				<AppRailAnchor href="/" target="_blank" title="Account">(icon)</AppRailAnchor>
			</svelte:fragment>
		</AppRail>
	</div>
{/if}

<!--
<AppBar>
	<svelte:fragment slot="lead"
		><button class="btn variant-filled" use:popup={popupClick}><AlignJustify /></button>
		<div class="card p-4 max-w-sm" data-popup="popupClick">
			<div class="grid grid-cols-1 gap-2">
				<button id="wont-close" class="btn variant-filled-error">Settings</button>
				<button id="will-close" class="btn variant-filled-success">Mobile</button>
				<button id="hello" class="btn variant-filled-success">About</button>
				<button id="hello" class="btn variant-filled-success">Chat</button>
				<button id="hello" class="btn variant-filled-success">Tips and Tricks</button>
			</div>
			<div class="arrow bg-surface-100-800-token" />
		</div></svelte:fragment
	>
	<GraduationCap />

	<svelte:fragment slot="trail"><BookCheck /></svelte:fragment>
</AppBar>
-->
