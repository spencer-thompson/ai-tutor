<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { marked } from 'marked';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';
	import { enhance, applyAction } from '$app/forms';

	export let data;

	let name = 'textarea',
		textarea = '',
		height = 120,
		value = ``,
		inputHeight = 0;

	let chatContainer;
	let isLoading = false;

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

	interface Message {
		role: string;
		content: string;
		name: string;
	}

	let messages: Message[] = [
		// { sender: role.user, message: 'this is a message from the user!' },
		// { sender: role.ai, message: marked.parse('# Marked in **the** *brower*') }
	];

	let buffer = '';

	async function readData() {
		console.log('calling');
		const payload = {
			messages: [
				{
					name: 'Joshua',
					role: 'user',
					content: value
				}
			],
			courses: [101, 202],
			model: 'gpt-4o'
		};

		try {
			const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'AITUTOR-API-KEY': data.apiKey,
					Authorization: `Bearer ${data.token}`
				},
				body: JSON.stringify(payload)
			});

			console.log(response.status);
			console.log(response.body);

			const decoder = new TextDecoder();

			if (response.body) {
				const reader = response.body.getReader();
				const processChunk = async () => {
					const { done, value } = await reader.read();

					if (done) {
						console.log('Streaming complete');
						return;
					}

					const decodedChunk = decoder.decode(value, { stream: true });
					// { role: 'assistant', content: `${buffer}`, name: 'ai' }
					const regex = /(?<="content":\s?")([^"]+)/g;

					const match = decodedChunk.match(regex);

					if (match) {
						for (let i = 0; i < match.length; i++) {
							buffer += match[i];
							if (messages.length > 0) {
								messages[messages.length - 1].content = buffer;
							}
						}
					}

					console.log(decodedChunk);
					console.log(match);

					await processChunk();
				};

				await processChunk();
			}
		} catch (error) {
			console.error('Streaming error:', error);
		}
		console.log(buffer);
	}

	function addMessage(role: string, text: string) {
		messages = [...messages, { role, content: text, name: 'user' }];
		console.log(text);

		// console.log(import.meta.env.VITE_API_KEY);

		setTimeout(() => {
			window.scrollTo(0, document.body.scrollHeight);
		}, 0);
	}

	async function sendMessage(role: string, text: string) {
		if (text.trim() != '') addMessage(role, text);
		readData();

		messages = [...messages, { role: 'assistant', content: `${buffer}`, name: 'ai' }];
		buffer = '';
		console.log(height);
		console.log(inputHeight);
		console.log(data.token);
		console.log(data.apiKey);

		value = '';
		isLoading = true;
	}
</script>

<!-- document.cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNjkzNzkwIiwidW5pIjoidXZ1IiwiZXhwIjoxNzM3NDQxMDkxLCJpYXQiOjE3MzczNTQ2OTF9.16z4uMY_eg5t0S7ihPvodklYzBTB-IVnquT08FhqHzo; expires=Fri, 30 Jan 2025 23:59:59 GMT; path=/"; -->

<!--style="margin-bottom: {120}px-->
<main class="flex flex-col min-h-screen overflow-y-auto">
	<div class="flex-1 flex flex-col-reverse" style="margin-bottom: {height + 90}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div transition:slide class="flex items-start gap-2.5 mb-4">
					<div
						transition:scale
						class="
                    max-w-[220px] py-1 px-3 rounded-lg {message.role === 'user'
							? ' ml-auto bg-blue-600 rounded-br-none'
							: ' mr-auto bg-gray-300 rounded-bl-none'}
                            "
					>
						<p
							class={message.role === 'user'
								? 'text-sm font-normal py-2.5 text-gray-900 dark:text-white'
								: 'text-sm font-normal py-2.5 text-gray-900 dark:text-black'}
						>
							{@html message.content}
						</p>
					</div>
				</div>
			{/each}
		</div>
	</div>
	<div class="bottom-48"></div>

	<div class="fixed gap-2 inset-x-0 bottom-10 mx-4">
		<div class="max-w-2xl mx-auto">
			<div class="bg-gray-100 rounded-3xl py-3 relative">
				<div class="flex flex-col w-full pr-24">
					<!--<form
						method="POST"
						action="?/send"
						use:enhance={() => {
							sendMessage('user', value);
							return async ({ update }) => {
								await update();
							};
						}}
					>
					</form>-->
					<textarea
						{rows}
						name="textareaContent"
						bind:this={textarea}
						use:resize
						on:resize={onResize}
						placeholder="Send message to AI Tutor..."
						style="--height: auto"
						bind:value
						class="flex-1 bg-transparent border-none outline-none min-h-[40px] max-h-[500px] text-black focus:ring-0"
					></textarea>
					<button
						on:click={() => {
							sendMessage('user', value);
						}}
						class=" absolute bottom-5 right-3 max-h-14 px-4 py-2 bg-blue-500 text-white rounded-xl focus:bg-blue-600"
						><SendHorizontal size="24" /></button
					>
				</div>
			</div>
		</div>
	</div>
</main>

<!--on:submit={() => sendMessage('user', value)}-->

<!--
		currentStreamingMessage = '';
		messages = [...messages, { role: 'assistant', content: '', name: 'assistant' }];

		const courses = [101, 202];

		try {
			const response = await fetch('/', {
				method: 'POST',
				body: JSON.stringify({
					// messages: messages,
					messages: messages.slice(0, -1),
					courses: courses
				}),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const reader = response.body?.getReader();
			const decoder = new TextDecoder();

			while (true) {
				const { done, value } = await reader!.read();
				if (done) break;

				const chunk = decoder.decode(value);
				currentStreamingMessage += chunk;

				messages = messages.map((msg, index) => {
					if (index === messages.length - 1) {
						return { ...msg, content: currentStreamingMessage };
					}
					return msg;
				});
			}
		} catch (error) {
			console.error('Error:', error);
			messages = messages.map((msg, index) => {
				if (index === messages.length - 1) {
					return { ...msg, content: 'Sorry, there waa an error processing your request.' };
				}
				return msg;
			});
		} finally {
			isLoading = false;
		}
-->

<!--on:submit={(event) => {
	event.preventDefault();
	sendMessage('user', value);
	event.currentTarget.submit();
}}-->

<style>
	textarea {
		height: var(--height);
		resize: none;
		padding: 1rem;
		line-height: 1.5;
		will-change: height;
		transition: rows 250ms ease;
		overflow: hidden;
		/* overflow-x: scroll; */
	}
</style>
