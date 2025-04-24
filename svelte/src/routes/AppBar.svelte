<script lang="ts">
	import {
		AppRail,
		AppRailTile,
		AppRailAnchor,
		AppBar,
		Modal,
		Drawer,
		getModalStore,
		getDrawerStore,
		popup
	} from '@skeletonlabs/skeleton';
	import type {
		DrawerSettings,
		DrawerStore,
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
		Lightbulb,
		PaintBucket
	} from 'lucide-svelte';
	import { fly, slide, scale, fade } from 'svelte/transition';
	import { bounceOut, cubicIn, cubicInOut, circOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import CourseSettingsModal from './CourseSettingsModal.svelte';
	import ThemeSettingsModal from './ThemeSettingsModal.svelte';

	const modalStore = getModalStore();
	const drawerStore = getDrawerStore();

	const modalCourses: ModalSettings = {
		type: 'component',
		component: 'courses'
		// meta: {
		// 	course_data: data.apiData
		// }
	};
	function openCoursesModal() {
		modalStore.close();
		modalStore.trigger(modalCourses);
	}

	const modalTheme: ModalSettings = {
		type: 'component',
		component: 'themes'
	};
	function openThemeModal() {
		modalStore.close();
		modalStore.trigger(modalTheme);
	}

	const drawer: DrawerSettings = {
		id: 'example-3',
		// Provide your property overrides:
		/*bgDrawer: 'bg-purple-900 text-white',*/
		meta: { foo: 'bar', fizz: 'buzz', age: 40 },
		bgDrawer: 'bg-surface-500 text-white',
		/*bgBackdrop: 'bg-gradient-to-tr from-indigo-500/50 via-purple-500/50 to-pink-500/50',*/
		bgBackdrop: 'bg-gradient-to-tr from-tertiary-500/50 to-primary-500/50',
		// width: 'w-[250px] md:w-[380px]',
		width: 'w-[250px]',
		height: 'bottom-3',
		regionDrawer: 'mt-20 ml-2 mb-3',

		rounded: 'rounded-xl'
	};
	function openDrawerModal() {
		drawerStore.open(drawer);
	}
	let currentTile: number = 0;
	let appRailVisible = true;
	let showAppBar = false;

	function updateAppRailVisibility() {
		appRailVisible = window.innerWidth < 1027 ? false : true;
		showAppBar = window.innerWidth <= 1027 ? true : false;
	}

	onMount(() => {
		updateAppRailVisibility();
		window.addEventListener('resize', updateAppRailVisibility);
		return () => window.removeEventListener('resize', updateAppRailVisibility);
	});
</script>

{#if !showAppBar}
	<div class="fixed z-10 p-3" transition:fly={{ x: -100, duration: 800 }}>
		<button
			class="btn-menu open"
			on:click|preventDefault={() => (appRailVisible = !appRailVisible)}
		>
			<div class="flex justify-center items-center w-full">
				<GraduationCap size="56" />
			</div>
		</button>
	</div>
	<div class="fixed right-2 z-10 p-3" transition:fly={{ x: 100, duration: 800 }}>
		<button on:click={openThemeModal}><PaintBucket /></button>
	</div>
{:else}
	<div class="fixed w-full z-50" in:fly={{ x: -50, duration: 800 }}>
		<AppBar>
			<svelte:fragment slot="lead"
				><button on:click={openDrawerModal}><GraduationCap size="36" /></button>
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
			<h3>AI Tutor Beta</h3>

			<svelte:fragment slot="trail"
				><button on:click={openThemeModal}><PaintBucket /></button></svelte:fragment
			>
		</AppBar>
	</div>
{/if}

{#if appRailVisible && !showAppBar}
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
				on:click={openCoursesModal}
			>
				<svelte:fragment slot="lead">
					<div class="flex justify-center items-center w-full">
						<BookCheck size="36" />
					</div>
				</svelte:fragment>
				<span>Courses</span>
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
