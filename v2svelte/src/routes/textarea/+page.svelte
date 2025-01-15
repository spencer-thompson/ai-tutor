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

<main class="flex flex-col min-h-screen">
	<div class="flex-1 flex flex-col-reverse mb-24">
		<div class="w-full max-w-2xl mx-auto px-4">
			{#each messages as message}
				<div class="flex items-start gap-2.5 mb-4">
					<div class={message.sender === Sender.user ? ' ml-auto' : 'mr-auto'}>
						<p class="text-sm font-normal py-2.5 text-gray-900 dark:text-white">
							{message.message}
							{count}
						</p>
					</div>
				</div>
			{/each}
		</div>
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
