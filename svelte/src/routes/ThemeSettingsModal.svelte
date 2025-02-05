<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { Check } from 'lucide-svelte';

	export let parent: SvelteComponent;
	const modalStore = getModalStore();

	let theme = 'vintage';

	function section(c: string): void {
		theme = c;
		// document.documentElement.setAttribute('data-theme', theme.toLowerCase());
	}
</script>

{#if $modalStore[0]}
	<div class="card p-4 w-modal shadow-xl space-y-4">
		<header class="text-2xl font-bold">Select Theme</header>
		<!--<button type="button" class="btn variant-filled"> Course1</button>-->

		<div class="flex flex-wrap gap-3">
			{#each ['skeleton', 'vintage', 'crimson'] as c}
				<button
					class="btn {theme === c ? 'variant-filled' : 'variant-soft'}"
					on:click={() => {
						section(c);
					}}
					on:keypress
				>
					{#if theme === c}<span><Check size="16" /></span>{/if}
					<span>{c}</span>
				</button>
			{/each}
		</div>
		<footer class="modal-footer {parent.regionFooter}">
			<button class="btn {parent.buttonPositive}" on:click={parent.onClose}>Confirm </button>
		</footer>
	</div>
{/if}
