<script lang="ts">
	import { resize } from '$lib/components/textarea/resize';
	// const { input, handleSubmit, messages } = useChat();
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

	enum Sender {
		user,
		ai
	}

	interface Message {
		sender: Sender;
		message: string;
	}

	let count: number[] = [0];
	let i = 1;

	let messages: Message[] = [{ sender: Sender.user, message: 'this is a message from the user!' }];

	function addMessage(sender: Sender, text: string) {
		messages = [...messages, { sender, message: text }];
		count.push(i);
		i += 1;
	}
</script>

<main class="flex flex-col-reverse">
	<div class="inset-x-0 bottom-10 flex justify-center flex-col">
		{#each messages as message}
			<div class="flex items-start gap-2.5 place-self-center justify-center">
				<div
					class="flex flex-col w-full max-w-[220px] leading-1.5 p-1 px-3 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700"
				>
					<p class="text-sm font-normal py-2.5 text-gray-900 dark:text-white">
						{message.message}
						{count}
					</p>
				</div>
			</div>
		{/each}
	</div>

	<div class="fixed inset-x-0 bottom-10 flex justify-center">
		<textarea
			{rows}
			bind:this={textarea}
			use:resize
			on:resize={onResize}
			placeholder="textarea"
			style="--height: auto"
			bind:value
			class="text-black rounded-lg"
		></textarea>
		<button on:click={() => addMessage(Sender.ai, 'this is an AI message')}>Click Here</button>
	</div>
</main>

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
