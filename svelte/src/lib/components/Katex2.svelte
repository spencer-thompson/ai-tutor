<script lang="ts">
	import { onMount } from 'svelte';
	export let displayMode: boolean = true;
	export interface KatexProps {
		displayMode?: boolean;
	}

	// Extract the math expression from the component's children (slot content)
	let math = '';

	// Listen for changes to the children and update the math variable accordingly
	onMount(() => {
		const handleSlotChange = () => {
			// Get the first child node (text node) and extract its value
			const nodes = document.querySelectorAll('slot:not([name])');
			if (nodes.length > 0 && nodes[0].firstChild?.textContent) {
				math = nodes[0].firstChild.textContent;
			}
		};

		// Add a mutation observer to detect changes in the children
		const obs = new MutationObserver(handleSlotChange);
		obs.observe(document.body, { childList: true });
	});
</script>

<slot />

<svelte:head>
	<link
		rel="stylesheet"
		href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"
		integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X"
		crossorigin="anonymous"
	/>
</svelte:head>

{@html katexString}
