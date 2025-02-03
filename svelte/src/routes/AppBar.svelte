<script lang="ts">
	import {
		AppRail,
		AppRailTile,
		AppRailAnchor,
		AppBar,
		Modal,
		getModalStore,
		popup
	} from '@skeletonlabs/skeleton';
	import type {
		ModalSettings,
		ModalComponent,
		ModalStore,
		PopupSettings
	} from '@skeletonlabs/skeleton';
	import {
		AlignJustify,
		BookCheck,
		GraduationCap,
		BotMessageSquare,
		TabletSmartphone,
		Settings,
		Info,
		Lightbulb
	} from 'lucide-svelte';
	import { fly, slide, scale } from 'svelte/transition';
	import { bounceOut, cubicIn, cubicInOut, circOut } from 'svelte/easing';

	const modalStore = getModalStore();

	const modal: ModalSettings = {
		type: 'confirm',
		title: 'Application Settings',
		body: 'Configure your application preferences here.'
		// Optional: Add buttons or custom content
	};

	function openSettingsModal() {
		modalStore.close();
		modalStore.trigger(modal);
	}

	let currentTile: number = 0;
	let appRailVisible = false;
</script>

<div class="fixed z-50 p-3">
	<button class="btn-menu open" on:click|preventDefault={() => (appRailVisible = !appRailVisible)}>
		<div class="flex justify-center items-center w-full">
			<GraduationCap size="56" />
		</div>
	</button>
</div>

<!--AlignJustify, BookCheck, GraduationCap, BotMessageSquare, TabletSmartphone, Settings, Info,
LightBulb-->

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
						<BotMessageSquare size="36" />
					</div>
				</svelte:fragment>
				<span>Chat</span>
			</AppRailTile>

			<AppRailTile
				AppRailTile
				bind:group={currentTile}
				name="tile-2"
				value={1}
				title="tile-2"
				on:click={openSettingsModal}
			>
				<svelte:fragment slot="lead">
					<div class="flex justify-center items-center w-full">
						<BookCheck size="36" />
					</div>
				</svelte:fragment>
				<span>Settings</span>
			</AppRailTile>

			<AppRailTile bind:group={currentTile} name="tile-3" value={2} title="tile-3">
				<svelte:fragment slot="lead">
					<div class="flex justify-center items-center w-full">
						<TabletSmartphone size="36" />
					</div>
				</svelte:fragment>
				<span>Mobile</span>
			</AppRailTile>

			<AppRailTile bind:group={currentTile} name="tile-4" value={3} title="tile-4">
				<svelte:fragment slot="lead">
					<div class="flex justify-center items-center w-full">
						<Settings size="36" />
					</div>
				</svelte:fragment>
				<span>Settings</span>
			</AppRailTile>

			<AppRailTile bind:group={currentTile} name="tile-5" value={4} title="tile-5">
				<svelte:fragment slot="lead">
					<div class="flex justify-center items-center w-full">
						<Lightbulb size="36" />
					</div>
				</svelte:fragment>
				<span>Tips</span>
			</AppRailTile>
			<svelte:fragment slot="trail">
				<AppRailTile bind:group={currentTile} name="tile-6" value={5} title="tile-6">
					<div class="flex justify-center items-center w-full">
						<Info size="36" />
					</div>
					<span>About</span>
				</AppRailTile>
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
