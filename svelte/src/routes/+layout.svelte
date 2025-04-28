<script lang="ts">
	import '../app.postcss';

	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';
	import { onMount } from 'svelte';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';
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

	export let data;

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('javascript', javascript);
	hljs.registerLanguage('typescript', typescript);
	storeHighlightJs.set(hljs);

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import {
		Modal,
		Drawer,
		getModalStore,
		getDrawerStore,
		initializeStores,
		storePopup
	} from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
	initializeStores(); // Initialize Skeleton stores
	import AppBar from './AppBar.svelte';
	import CourseSettingsModal from './CourseSettingsModal.svelte';
	import ThemeSettingsModal from './ThemeSettingsModal.svelte';

	const modalRegistry: Record<string, ModalComponent> = {
		courses: { ref: CourseSettingsModal },
		themes: { ref: ThemeSettingsModal }
	};

	const modalStore = getModalStore();
	const drawerStore = getDrawerStore();

	let showAppBar = false;

	function updateAppRailVisibility() {
		if (window.innerWidth > 1027 && $drawerStore.id === 'example-3') {
			drawerStore.close();
		}
		// showAppBar = window.innerWidth < 1027 ? true : false;
	}

	onMount(() => {
		updateAppRailVisibility();
		window.addEventListener('resize', updateAppRailVisibility);
		return () => window.removeEventListener('resize', updateAppRailVisibility);
	});
</script>

<AppBar />

<slot />

<Modal components={modalRegistry} />
<Drawer>
	<div out:fade>
		{#if $drawerStore.id === 'example-3'}
			<div class="p-4">
				<h2 class="text-xl font-bold mb-4">Brought to you by:</h2>
				<p class="mb-4">The OG AI-Tutor Team</p>
				<div class="flex flex-col gap-3">
					<button on:click={drawerStore.close} class="btn variant-filled-primary"
						><div class="flex gap-2">
							<h4>Chat</h4>
							<BotMessageSquare />
						</div>
					</button>
					<button on:click={drawerStore.close} class="btn variant-filled-primary">
						<div class="flex gap-2">
							<h4>Courses</h4>
							<BookCheck />
						</div>
					</button>
					<button on:click={drawerStore.close} class="btn variant-filled-primary">
						<div class="flex gap-2">
							<h4>Mobile</h4>
							<TabletSmartphone />
						</div>
					</button>

					<button on:click={drawerStore.close} class="btn variant-filled-primary">
						<div class="flex gap-2">
							<h4>Settings</h4>
							<Settings />
						</div>
					</button>

					<button on:click={drawerStore.close} class="btn variant-filled-primary">
						<div class="flex gap-2">
							<h4>Tips</h4>
							<Lightbulb />
						</div>
					</button>
					<button on:click={drawerStore.close} class="btn variant-filled-primary">
						<div class="flex gap-2">
							<h4>About</h4>
							<Info />
						</div>
					</button>
				</div>
			</div>
		{/if}
	</div>
</Drawer>
