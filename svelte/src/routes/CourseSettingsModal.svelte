<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { Check } from 'lucide-svelte';
	import { userData } from '$lib/stores/userDataStore';

	export let parent: SvelteComponent;
	export let data;
	const modalStore = getModalStore();
	let color = 'red';

	let flavors: Record<string, boolean> = {
		course1: true,
		course2: false,
		course3: false,
		course4: true,
		course5: false,
		course6: true,
		course7: false
	};

	function toggle(flavor: string): void {
		flavors[flavor] = !flavors[flavor];
	}
</script>

{#if $modalStore[0]}
	<pre>{JSON.stringify($userData, null, 2)}</pre>
	<!-- {JSON.stringify(., null, 2)} -->
	<div class="card p-4 w-modal shadow-xl space-y-4">
		<header class="text-2xl font-bold">Select Courses</header>
		<!--<button type="button" class="btn variant-filled"> Course1</button>-->
		<div class="flex flex-wrap gap-3">
			{#each Object.keys(flavors) as f}
				<button
					class="btn {flavors[f] ? 'variant-filled' : 'variant-soft'}"
					on:click={() => {
						toggle(f);
					}}
					on:keypress
				>
					{#if flavors[f]}<span><Check size="16" /></span>{/if}
					<span class="capitalize">{f}</span>
				</button>
			{/each}
		</div>
		<footer class="modal-footer {parent.regionFooter}">
			<!--<button class="btn {parent.buttonNeutral}" on:click={parent.onClose}
				>{parent.buttonTextCancel}</button
			>-->
			<button class="btn {parent.buttonPositive}" on:click={parent.onClose}>Confirm </button>
		</footer>
	</div>
{/if}
