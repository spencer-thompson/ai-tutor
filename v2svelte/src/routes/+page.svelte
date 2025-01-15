<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { marked } from 'marked';
	let name = 'textarea',
		textarea = '',
		height = 120,
		value = ``,
		inputHeight = 0;

	function onResize(event) {
		const { detail } = event;
		if (detail.CR) {
			// console.log(e);
			inputHeight = detail.CR.height;
			textarea = event.target;
			height = event.detail.CR.height;
		}
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

	let messages: Message[] = [
		{ sender: Sender.user, message: 'this is a message from the user!' },
		{ sender: Sender.ai, message: marked.parse('# Marked in **the** *brower*') }
	];

	function addMessage(sender: Sender, text: string) {
		messages = [...messages, { sender, message: text }];
		console.log(text);
		setTimeout(() => {
			window.scrollTo(0, document.body.scrollHeight);
		}, 0);
	}

	//This is the next part I am working on:
	async function sendMessage(sender: Sender, text: string) {
		if (text != '') addMessage(Sender.user, value);
		value = '';

		// const courses = [101, 202];
		//
		// let requestBody = {
		// 	messages: messages,
		// 	courses: courses
		// };
		//
		// const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
		// 	method: 'POST',
		// 	body: JSON.stringify({
		// 		userId: 1,
		// 		title: 'I guess stuff goes here',
		// 		completed: false
		// 	}),
		// 	headers: {
		// 		'Content-Type': 'application/json',
		// 		'AITUTOR-API-KEY': '${headerManager.apiKey}',
		// 		Authorization: 'Bearer ${headerManager.jwt}'
		// 	}
		// });
		// for await (const chunk of response.body) {
		// 	console.log(chunk);
		// }
	}

	//check out basic_chat_ui.dart in playground!!!
	//Need to verify syntax, also, do I need the qr code?
</script>

<main class="flex flex-col min-h-screen">
	<div class="flex-1 flex flex-col-reverse mb-24" style="margin-bottom: {inputHeight + 90}px">
		<div class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div class="flex items-start gap-2.5 mb-4">
					<div
						class="
                    max-w-[220px] py-1 px-3 rounded-lg {message.sender === Sender.user
							? ' ml-auto bg-blue-600 rounded-br-none'
							: ' mr-auto bg-gray-300 rounded-bl-none'}
                            "
					>
						<p
							class={message.sender === Sender.user
								? 'text-sm font-normal py-2.5 text-gray-900 dark:text-white'
								: 'text-sm font-normal py-2.5 text-gray-900 dark:text-black'}
						>
							{@html message.message}
						</p>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<div class="fixed gap-2 inset-x-0 bottom-10 mx-4">
		<div class="max-w-2xl mx-auto">
			<div class="bg-gray-100 rounded-3xl py-3 relative">
				<div class="flex flex-col w-full pr-24">
					<textarea
						{rows}
						bind:this={textarea}
						use:resize
						on:resize={onResize}
						placeholder="Send message to AI Tutor..."
						style="--height: auto"
						bind:value
						class="flex-1 bg-transparent border-none outline-none min-h-[40px] max-h-[500px] text-black focus:ring-0"
					></textarea>
					<button
						on:click={() => sendMessage(Sender.user, textarea.value)}
						class=" absolute bottom-5 right-3 max-h-14 px-4 py-2 bg-blue-500 text-white rounded-xl focus:bg-blue-600"
						><SendHorizontal size="24" /></button
					>
				</div>
			</div>
		</div>
	</div>
</main>

<style>
	textarea {
		height: var(--height);
		resize: none;
		padding: 1rem;
		line-height: 1.5;
		/* overflow: hidden; */
		/* overflow-x: scroll; */
	}
</style>
