<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';
	import { clipboard, Avatar } from '@skeletonlabs/skeleton';
	import { decodeUnicode } from '$lib/utils/decodeUnicode';
	import MarkdownExample from './MarkdownExample.svelte';
	import { onMount } from 'svelte';
	import Katex from '$lib/components/Katex.svelte';
	import Katex2 from '$lib/components/Katex2.svelte';
	import { marked } from 'marked';
	import markedKatex from 'marked-katex-extension';

	const math1 = 'ax^2+bx+c=0';
	const math2 = 'x=-\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}';
	const math3 = 'V=\\frac{1}{3}\\pi r^2 h';

	export let data;

	let y: number;

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

	let messages: Message[] = [{ role: 'user', content: '\int\cos^3(x)\,dx', name: 'Guts' }];

	let buffer = '';
	let scrollBufferHeight = 30;

	$: rows = (value.match(/\n/g) || []).length + 1 || 1;

	function scrolldown() {
		if (document.body.scrollHeight - (window.innerHeight + y) < scrollBufferHeight) {
			setTimeout(function () {
				window.scrollTo(0, document.body.scrollHeight);
				scrolldown();
			}, 0);
		}
	}

	async function readData() {
		console.log('calling');
		const payload = {
			messages,
			courses: [101, 202],
			model: 'gpt-4o'
		};

		try {
			buffer = '';
			const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'AITUTOR-API-KEY': data.apiKey,
					Authorization: `Bearer ${data.token}`
				},
				body: JSON.stringify(payload)
			});

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
		messages[messages.length - 1].content = buffer;
		scrollBufferHeight = 30;
	}

	function addMessage(role: string, text: string) {
		messages = [...messages, { role, content: text, name: 'Joshua' }];
		readData();

		messages = [...messages, { role: 'assistant', content: '', name: 'ai' }];

		console.log(text);
	}

	async function sendMessage(role: string, text: string) {
		if (text.trim() != '') addMessage(role, text);
		setTimeout(() => {
			scrollBufferHeight = 10;
		}, '300');
		scrolldown();
		value = '';
	}

	const options = {
		throwOnError: false
	};

	marked.use(markedKatex(options));

	const parsedContent = marked.parse('katex: $c = \\pm\\sqrt{a^2 + b^2}$');
</script>

<svelte:head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.7/katex.min.css" />
</svelte:head>

<!-- document.cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNjkzNzkwIiwidW5pIjoidXZ1IiwiZXhwIjoxNzM4NTkzODQ3LCJpYXQiOjE3Mzg1MDc0NDd9.6-KGzKfetoEOM_c-vJaXDYS-YQq_FbKHlhJS0vflqpM; expires=Fri, 28 Feb 2025 23:59:59 GMT; path=/"; -->

<main class="flex flex-col min-h-screen">
	<Katex math="ax^2+bx+c=0" />
	<Katex math={math3} displayMode={true} />
	<Katex math="\int\cos^3(x)\,dx" />
	<div>{@html marked.parse('$\\int\\cos^3(x)\dx$')}</div>
	<div>{@html marked.parse('katex: $c = \\pm\\sqrt{a ^ (2 + b) ^ 2}$')}</div>

	<Katex math="cos^3(x)" displayMode={true} />
	<Katex math="\cos^3(x) = \cos(x) \cdot (1 - \sin^2(x))" displayMode={true} />
	<MarkdownExample />
	<div class="flex-1 flex flex-col-reverse overflow-y-auto" style="margin-bottom: {height + 90}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div transition:slide class="flex items-start gap-2.5 mb-4">
					{#if message.role === 'assistant'}{/if}
					<div
						transition:scale
						class="
                    max-w-[620px] px-3 rounded-lg {message.role === 'user'
							? ' ml-auto bg-blue-600 rounded-br-none'
							: ' mr-auto bg-gray-300 rounded-bl-none'}
                            "
					>
						<p
							class={message.role === 'user'
								? 'text-sm font-normal py-2.5 text-gray-900 dark:text-white'
								: 'text-sm font-normal py-2.5 text-gray-900 dark:text-black'}
						>
							{@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))}
							<!--{@html message.content}-->
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
							sendMessage('user', textarea.value);
						}}
						class=" absolute bottom-5 right-3 max-h-14 px-4 py-2 bg-blue-500 text-white rounded-xl focus:bg-blue-600"
						><SendHorizontal size="24" /></button
					>
				</div>
			</div>
		</div>
	</div>
</main>

<svelte:window bind:scrollY={y} />

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
