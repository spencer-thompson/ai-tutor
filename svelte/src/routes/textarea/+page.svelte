<script>
	export let data;
</script>

<a href="/">Home</a>

<h2>Data streamed</h2>

<h2>minimalData</h2>
{@html data.minimalData}

<h2>biggerData</h2>
{@html data.biggerData}

<h2>hugeData</h2>
{#await data.hugeData}
	<!-- showing this div only to users who have JavaScript enabled -->
	<div class="jsonly">Loading ...</div>
	<!-- showing this noscript tag only to users who do not have JavaScript -->
	<noscript>
		<style>
			.jsonly {
				display: none !important;
			}
		</style>
		<a href="/stream?noJS=true">Load the rest</a>
	</noscript>
{:then hugeData}
	{@html hugeData}
{/await}
