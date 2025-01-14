<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->
<script lang="ts">
	import Chat from '$lib/components/chat/Scheduler.svelte';
	import { resize } from '$lib/components/textarea/resize';

	import { useChat } from '@ai-sdk/svelte';

	const { input, handleSubmit, messages } = useChat();
	// let inputValue = '';
	let rows = 1;

	function adjustHeight(event) {
		const textarea = event.target;
		textarea.style.height = 'auto';
		textarea.style.height = `{textarea.scrollheight}px`;
	}

	// function handleSubmit() {
	// 	console.log('Message was submitted');
	// }

	let name = 'textarea',
		textarea = null,
		height = 120,
		inputValue = `value \nvalue 2 \nvalue 3`;

	function onResize(e) {
		// console.log(e);
		textarea = e.target;
		height = e.detail.CR.height;
	}

	$: rows = (inputValue.match(/\n/g) || []).length + 1 || 1;
	// This calculates the number of rows needed based on newline chars. (default is 1)

	// $: console.log(value, rows);
	// logs rows and values upon updating
</script>

<main class="flex flex-col h-screen">
	<ul>
		{#each $messages as message}
			<li>
				{message.role}:
				{#if message.toolInvocations}
					<pre>{JSON.stringify(message.toolInvocations, null, 2)}</pre>
				{:else}
					<div class="flex items-start gap-2.5">
						<div
							class="flex flex-col w-full max-w-[220px] leading-1.5 p-1 px-3 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700"
						>
							<p class="text-sm font-normal py-2.5 text-gray-900 dark:text-white">
								{message.content}
							</p>
						</div>
					</div>
				{/if}
			</li>
		{/each}
	</ul>

	<div class="flex items-start gap-2.5">
		<form
			class="decoration-black max-w-[220px] flex flex-col w-full leading-1.5"
			on:submit={handleSubmit}
		>
			<div class="fixed inset-x-0 bottom-10 flex justify-center">
				<textarea
					class="resize-none rounded-lg text-sky-400 bg-black decoration-red p-2 h-auto max-h-[300px] overflow-y-auto"
					{rows}
					bind:this={textarea}
					use:resize
					on:resize={onResize}
					placeholder="textarea"
					style="--height: auto"
					bind:value={$input}
				/>
				<button class="subButton" type="submit">Send</button>
			</div>
		</form>
	</div>
	<!--<Chat />-->
</main>

<!--class="rounded-lg text-sky-400 bg-black decoration-red"-->

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

	:global(body) {
		background: #000;
	}

	main {
		width: 500px;
		margin: 50px auto;
	}

	.subButton {
		color: white;
	}

	.customBox {
		color: white;
		background: blue;
	}
</style>
