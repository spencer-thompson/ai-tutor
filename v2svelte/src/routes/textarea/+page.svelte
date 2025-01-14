<script lang="ts">
	import { resize } from '$lib/components/textarea/resize';
	let name = 'textarea',
		textarea = null,
		height = 120,
		value = `value \nvalue 2 \nvalue 3`;

	function onResize(e) {
		// console.log(e);
		textarea = e.target;
		height = e.detail.CR.height;
	}

	$: rows = (value.match(/\n/g) || []).length + 1 || 1;
	// This calculates the number of rows needed based on newline chars. (default is 1)

	// $: console.log(value, rows);
	// logs rows and values upon updating
</script>

<textarea
	{rows}
	bind:this={textarea}
	use:resize
	on:resize={onResize}
	placeholder="textarea"
	style="--height: auto"
	bind:value
	class="text-black"
></textarea>

<style>
	span {
		color: red;
	}
	textarea {
		height: var(--height);
		resize: none;
		padding: 1rem;
		line-height: 1.5;
		/* overflow: hidden; */
		/* overflow-x: scroll; */
	}
</style>
