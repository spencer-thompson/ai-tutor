<script>
	// import Component
	import Katex from './katex.svelte';

	// math equations
	const math1 = 'ax^2+bx+c=0';
	const math2 = 'x=-\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}';
	const math3 = 'V=\\frac{1}{3}\\pi r^2 h';

	// set up array and index for reactivity and initialize
	const mathArray = [math1, math2, math3];
	let index = 0;
	$: math = mathArray[index];

	// changeMath function for button click
	function changeMath() {
		// increase index
		index = (index + 1) % 3;
	}
</script>

<h1>KaTeX svelte component demo</h1>

<h2>Inline math</h2>
Our math equation: <Katex {math} /> and it is inline.

<h2>Displayed math</h2>
Our math equation: <Katex {math} displayMode /> and it is displayed.

<h2>Reactivity</h2>
<button on:click={changeMath}>
	Displaying equation {index}
</button>

<h2>Static math expression within HTML</h2>
<Katex math={'V=\\pi\\textrm{ m}^3'} />

<h2>Slot based Svelte Component</h2>
Check out<a rel="external" href="https://www.npmjs.com/package/svelte-katex">Svelte KaTeX</a> for an
implementation of a Svelte KaTeX component that takes markup via slots

<h2>Disucssion of various approaches</h2>
Visit<a rel="external" href="https://svelte-math.vercel.app">Svelte Math</a> to see a discussion of various
ways to implement math in Svelte/SvelteKit.

<style>
	a {
		background-color: lightgray;
		text-decoration: underline;
		font-weight: 700;
		padding: 0.5em;
	}
</style>
