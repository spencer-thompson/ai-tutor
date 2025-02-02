<script lang="ts">
	import katex from 'katex';
	import 'katex/dist/katex.min.css';

	export let math = '';
	export let displayMode = false;

	let element;

	$: {
		if (element) {
			katex.render(math, element, {
				throwOnError: false,
				displayMode: displayMode
			});
		}
	}
</script>

<span bind:this={element}></span>
