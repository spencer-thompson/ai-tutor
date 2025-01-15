<script lang="ts">
	import { resize } from '$lib/components/textarea/resize';
	// const { input, handleSubmit, messages } = useChat();
	let name = 'textarea',
		textarea = null,
		height = 120,
		value = ``;

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
		<div class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div class="flex items-start gap-2.5 mb-4">
					<div
						class="
                    max-w-[220px] p-3 rounded-lg {message.sender === Sender.user
							? ' ml-auto bg-blue-600 rounded-br-none'
							: ' mr-auto bg-gray-300 rounded-bl-none'}
                            "
					>
						<p
							class={message.sender === Sender.user
								? 'text-sm font-normal py-2.5 text-gray-900 dark:text-white'
								: 'text-sm font-normal py-2.5 text-gray-900 dark:text-black'}
						>
							{message.message}
							{count}
						</p>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<div class="fixed gap-2 inset-x-0 bottom-10 flex justify-center">
		<textarea
			{rows}
			bind:this={textarea}
			use:resize
			on:resize={onResize}
			placeholder="Send message to AI Tutor..."
			style="--height: auto"
			bind:value
			class="flex-1 min-h-[44px] max-h-[200px] p-2 border rounded-lg resize-none text-black"
		></textarea>
		<button
			on:click={() => addMessage(Sender.user, 'this is an AI message')}
			class="px-4 py-2 bg-blue-500 text-white rounded-lg">Click Here</button
		>
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
