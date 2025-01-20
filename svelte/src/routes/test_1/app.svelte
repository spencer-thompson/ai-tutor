<script>
	import IntersectionObserver from './IntersectionObserver.svelte';
</script>

<IntersectionObserver let:intersecting top={400}>
	{#if intersecting}
		<section class="somesection">
			<div class="content">
				<h3>This message will show if it is intersecting.</h3>
				<p>
					Obviously you won't see it if it isn't, so better open up the console to see the changes.
				</p>
			</div>
		</section>
	{:else}
		<section class="somesection">
			This message will show if the section isn't intersecting. Hello from the console! 👀
		</section>
	{/if}
</IntersectionObserver>
<IntersectionObserver let:intersecting top={400}>
	{#if intersecting}
		<section class="somesection even">
			<div class="content">
				<h3>This message will show if it is intersecting.</h3>
				<p>
					Obviously you won't see it if it isn't, so better open up the console to see the changes.
				</p>
			</div>
		</section>
	{:else}
		<section class="somesection">
			This message will show if the section isn't intersecting. Hello from the console! 👀
		</section>
	{/if}
</IntersectionObserver>
<IntersectionObserver let:intersecting top={400}>
	{#if intersecting}
		<section class="somesection">
			<div class="content">
				<h3>This message will show if it is intersecting.</h3>
				<p>
					Obviously you won't see it if it isn't, so better open up the console to see the changes.
				</p>
			</div>
		</section>
	{:else}
		<section class="somesection">
			This message will show if the section isn't intersecting. Hello from the console! 👀
		</section>
	{/if}
</IntersectionObserver>
<IntersectionObserver let:intersecting top={400}>
	{#if intersecting}
		<section class="somesection even">
			<div class="content">
				<h3>This message will show if it is intersecting.</h3>
				<p>
					Obviously you won't see it if it isn't, so better open up the console to see the changes.
				</p>
			</div>
		</section>
	{:else}
		<section class="somesection">
			This message will show if the section isn't intersecting. Hello from the console! 👀
		</section>
	{/if}
</IntersectionObserver>

<style>
	.somesection {
		width: 100%;
		height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.somesection.even {
		background: #ccc;
	}

	.content {
		text-align: center;
		width: 350px;
	}
</style>
