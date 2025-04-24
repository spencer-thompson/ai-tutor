<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { Check } from 'lucide-svelte';
	import { userData } from '$lib/stores/userDataStore';

	export let parent: SvelteComponent;
	const modalStore = getModalStore();
	let color = 'red';

	let course_booleans: Record<string, boolean> = {};

	const regex = /^([^-\s]+-[^-\s]+)(?:-.*)?$/;
	let courses = $userData.courses;
	for (let i = 0; i < courses.length; i++) {
		const match = courses[i].name.match(regex);
		if (match && match[1]) {
			console.log(match[1]);
			course_booleans[match[1]] = true;
		} else {
			console.log(courses[i].name);
			course_booleans[courses[i].name] = true;
		}
	}

	// console.log($userData.courses.length);
	// JSON.stringify($userData, null, 2)

	function toggle(courseName: string): void {
		course_booleans[courseName] = !course_booleans[courseName];
	}
</script>

{#if $modalStore[0]}
	<!-- {courses} -->
	<!-- <pre>{JSON.stringify($userData.courses, null, 2)}</pre> -->
	<!-- <pre>{JSON.stringify($userData, null, 2)}</pre> -->
	<!-- {JSON.stringify(., null, 2)} -->
	<div class="card p-4 w-modal shadow-xl space-y-4">
		<header class="text-2xl font-bold">Select Courses</header>
		<!--<button type="button" class="btn variant-filled"> Course1</button>-->
		<div class="flex flex-wrap gap-3">
			{#each Object.keys(course_booleans) as f}
				<button
					class="btn {course_booleans[f] ? 'variant-filled' : 'variant-soft'}"
					on:click={() => {
						toggle(f);
					}}
					on:keypress
				>
					{#if course_booleans[f]}<span><Check size="16" /></span>{/if}
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
