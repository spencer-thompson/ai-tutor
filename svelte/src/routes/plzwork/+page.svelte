<script>
	import { onMount } from 'svelte';
	import katex from 'katex';

	let mathContainer;

	onMount(() => {
		if (mathContainer) {
			katex.render(String.raw`c = \pm\sqrt{a^2 + b^2}`, mathContainer, {
				throwOnError: false
			});
		}
	});
</script>

<svelte:head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.7/katex.min.css" />
</svelte:head>

<!-- Where the math formula will be displayed -->
<div bind:this={mathContainer}></div>
