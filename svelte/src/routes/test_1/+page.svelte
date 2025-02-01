<script lang="ts">
	import { fade } from 'svelte/transition';
	import ChatMessage from '$lib/components/ChatMessages.svelte';
	import ChatInput from '$lib/components/ChatInput.svelte';
	import type { Message } from '$lib/types/message';
	import { setupMarked } from '$lib/utils/markdown';
	import { streamChat } from '$lib/api/chat';

	export let data;

	setupMarked();

	let messages: Message[] = [
		{ role: 'user', content: 'this is a message from the user!', name: 'Guts' },
		{
			role: 'assistant',
			content: '# Hi! How can I assist you today?',
			name: 'ai'
		}
	];

	let y: number;
	let buffer = '';
	let scrollBufferHeight = 30;

	function scrolldown() {
		if (document.body.scrollHeight - (window.innerHeight + y) < scrollBufferHeight) {
			setTimeout(function () {
				window.scrollTo(0, document.body.scrollHeight);
				scrolldown();
			}, 0);
		}
	}

	function copyHandler(message: string) {
		console.log(message);
	}

	async function handleChatStream() {
		try {
			buffer = '';
			const response = await streamChat(messages, data.apiKey, data.token);

			if (response.body) {
				const reader = response.body.getReader();
				const decoder = new TextDecoder();

				const processChunk = async () => {
					const { done, value } = await reader.read();

					if (done) {
						console.log('Streaming complete');
						return;
					}

					const decodedChunk = decoder.decode(value, { stream: true });
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

					scrolldown();
					await processChunk();
				};

				await processChunk();
			}
		} catch (error) {
			console.error('Streaming error:', error);
		}

		messages[messages.length - 1].content = buffer;
		scrollBufferHeight = 30;
	}

	async function sendMessage(text: string) {
		if (text.trim() === '') return;

		messages = [
			...messages,
			{ role: 'user', content: text, name: 'Joshua' },
			{ role: 'assistant', content: '', name: 'ai' }
		];

		handleChatStream();

		setTimeout(() => {
			scrollBufferHeight = 10;
		}, 300);

		scrolldown();
	}
</script>

<main class="flex flex-col min-h-screen">
	<div class="flex-1 flex flex-col-reverse overflow-y-auto" style="margin-bottom: {120 + 90}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<ChatMessage {message} onCopy={copyHandler} />
			{/each}
		</div>
	</div>
	<ChatInput onSend={sendMessage} />
</main>

<svelte:window bind:scrollY={y} />
