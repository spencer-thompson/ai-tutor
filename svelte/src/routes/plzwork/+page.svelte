<script lang="ts">
	import { marked } from 'marked';
	import markedKatex from 'marked-katex-extension';

	const options = {
		throwOnError: false
	};

	marked.use(markedKatex(options));

	const parsedContent = marked.parse('katex: $c = \\pm\\sqrt{a^2 + b^2}$');
</script>

<svelte:head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.7/katex.min.css" />
</svelte:head>

<main>
	<div>{@html parsedContent}</div>
</main>
