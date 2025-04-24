<script lang="ts">
	import { SendHorizontal, MoveDown, SquareArrowDownLeft, SquareArrowUpRight } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';
	import { clipboard, Avatar } from '@skeletonlabs/skeleton';
	import { decodeUnicode } from '$lib/utils/decodeUnicode';
	import MarkdownExample from './MarkdownExample.svelte';
	import { onMount } from 'svelte';
	import { marked } from 'marked';
	import markedKatex from 'marked-katex-extension';
	import { markedHighlight } from 'marked-highlight';
	import hljs from 'highlight.js';

	export let data;

	let y: number;

	let name = 'textarea',
		textarea = '',
		height = 120,
		value = ``,
		inputHeight = 0,
		full_rows = 3,
		expanded = false,
		isFocused = false;

	function onResize(event) {
		const { detail } = event;
		if (detail.CR) {
			// console.log(e);
			inputHeight = detail.CR.height;
			textarea = event.target;
			height = event.detail.CR.height;
		}
	}

	const onFocus = () => (isFocused = true);
	const onBlur = () => (isFocused = false);

	let shouldShowButton = false;
	let showAppBar = false;

	function updateAppRailVisibility() {
		showAppBar = window.innerWidth < 1027 ? true : false;
	}

	onMount(() => {
		updateAppRailVisibility();
		window.addEventListener('resize', updateAppRailVisibility);
		return () => window.removeEventListener('resize', updateAppRailVisibility);
	});

	onMount(() => {
		window.addEventListener('scroll', () => {
			shouldShowButton = document.body.scrollHeight - (window.innerHeight + y) > window.innerHeight;
		});
	});

	let messages: Message[] = [];

	let buffer = '';
	let scrollBufferHeight = 30;

	$: rows = ((value.match(/\n/g) || []).length + 1) | full_rows;
	$: full_rows = expanded ? 30 : 3;

	let canScrollDown = true;

	function scrolldown() {
		if (
			document.body.scrollHeight - (window.innerHeight + y) < scrollBufferHeight &&
			canScrollDown
		) {
			setTimeout(function () {
				window.scrollTo(250, document.body.scrollHeight);
				scrolldown();
			}, 0);
			// setTimeout(function () {
			// 	window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
			// }, 0);
		}
	}

	function scrollup() {
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}

	// Replace \n inside LaTeX expressions with real newlines
	// const formatLatexMath = (str) =>
	// 	str.replace(/(\${1,2})([\s\S]*?)\1/g, (_, delim, content) => {
	// 		const fixed = content.replace(/\\n\s*/g, '\n');
	// 		return `${delim}${fixed}${delim}`;
	// 	});

	const formatLatexMath = (str) =>
		str.replace(/(\${1,2})\s*([\s\S]*?)\s*\1/g, (_, delim, content) => {
			const trimmed = content.trim().replace(/\\n\s*/g, '\n');
			return `${delim}${trimmed}${delim}`;
		});

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
						canScrollDown = false;
						return;
					}
					const decodedChunk = decoder.decode(value, { stream: true });

					const cleanedChunk = decodedChunk.replace(/(?<=\$+)\\\\/g, '\\').replace(/\\\\/g, '\\');

					const regex = /(?<="content":\s?")([^"]+)/g;

					const match = cleanedChunk.match(regex);

					const matchList = match ? Array.from(match) : [];

					if (matchList) {
						for (let i = 0; i < matchList.length; i++) {
							buffer += matchList[i];
							if (messages.length > 0) {
								console.log(`Match here: ${matchList}, length: ${matchList.length}`);
								console.log(`Match here: ${matchList[i]}`);

								// messages[messages.length - 1].content = marked.parse(decodeUnicode(buffer));

								messages[messages.length - 1].content = marked.parse(
									decodeUnicode(formatLatexMath(buffer.replace(/\\n/g, '\n')))
								);

								// {@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))}

								// {@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))}
							}
						}
					}

					// if (match) {
					// 	for (let i = 0; i < match.length; i++) {
					// 		buffer += match[i];
					// 		if (messages.length > 0) {
					// 			console.log(`Match here: ${match}, length: ${match.length}`);
					//
					// 			// messages[messages.length - 1].content = marked.parse(decodeUnicode(buffer));
					//
					// 			messages[messages.length - 1].content = marked.parse(
					// 				decodeUnicode(formatLatexMath(buffer))
					// 			);
					//
					// 			// {@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))}
					//
					// 			// {@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))}
					// 		}
					// 	}
					// }
					scrolldown();

					console.log(decodedChunk);
					// console.log(match);

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
	// $$ \n\int_{a}^{b} f(x) \, dx = F(b) - F(a)$$
	// $$ \int_{a}^{b} f(x) \, dx = F(b) - F(a) $$
	// ($ \int_{a}^{b} f(x) \, dx $)
	// $ \int_{a}^{b} f(x) \, dx $

	function addMessage(role: string, text: string) {
		messages = [...messages, { role, content: text, name: 'Joshua' }];
		readData();

		messages = [...messages, { role: 'assistant', content: '', name: 'ai' }];

		console.log(text);
	}

	async function sendMessage(role: string, text: string) {
		if (text.trim() != '') addMessage(role, text);
		canScrollDown = true;
		expanded = false;

		setTimeout(() => {
			scrollBufferHeight = 10;
		}, '300');
		scrolldown();
		// scrollup();
		value = '';
	}

	function expandTextArea() {
		expanded = !expanded;
	}

	const options = {
		throwOnError: false,
		nonStandard: true
	};

	marked.use(markedKatex(options));
	marked.use(
		markedHighlight({
			langPrefix: 'hljs language-',
			highlight(code, lang) {
				if (lang && hljs.getLanguage(lang)) {
					try {
						return hljs.highlight(code, { language: lang }).value;
					} catch {}
				}
				return hljs.highlightAuto(code).value;
			}
		})
	);
	marked.use({ breaks: true });

	const parsedContent = marked.parse('katex: $c = \\pm\\sqrt{a^2 + b^2}$');
</script>

<svelte:body data-sveltekit-preload-data="hover" data-theme="crimson" />

<svelte:head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.7/katex.min.css" />
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/styles/github-dark.min.css"
	/>
</svelte:head>

<!-- document.cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNjkzNzkwIiwidW5pIjoidXZ1IiwiZXhwIjoxNzQ1NDkxMTMxLCJpYXQiOjE3NDU0MDQ3MzF9.B1mpOmHk40eHO83qMxOdEQ1rr79SQpzFIsZ6zJ4SAYQ; expires=Fri, 28 May  2025 23:59:59 GMT; path=/"; -->

<main class="flex flex-col min-h-screen pt-30">
	<!--{#if shouldShowButton}-->

	{#if shouldShowButton}
		{#if !showAppBar}
			<div in:fly={{ y: 80, duration: 1000 }} out:fade class="fixed place-self-center top-3">
				<button
					on:click={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}
					class=" btn btn-sm rounded-xl bg-primary-500"><MoveDown /></button
				>
			</div>
		{:else}
			<div
				in:fly={{ y: -100, duration: 1000 }}
				out:fade
				class="z-51 fixed place-self-center top-20"
			>
				<button
					on:click={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}
					class=" btn btn-sm rounded-xl bg-primary-500"><MoveDown /></button
				>
			</div>
		{/if}
	{/if}

	<!--{#if !showAppBar}
		<div in:fly={{ y: 70, duration: 100 }} class="z-51 fixed place-self-center top-3">
			<button
				on:click={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}
				class=" btn btn-sm rounded-xl bg-tertiary-500"><MoveDown /></button
			>
		</div>
	{:else}
		<div in:fly={{ y: -100, duration: 1000 }} class="z-51 fixed place-self-center top-20">
			<button
				on:click={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}
				class=" btn btn-sm rounded-xl bg-tertiary-500"><MoveDown /></button
			>
		</div>
	{/if}

	<!--<MarkdownExample />-->
	{#if !showAppBar}
		<h1 in:fly={{ y: -100, duration: 1000 }} class="ml-24 mt-3">AI Tutor Beta</h1>
	{/if}
	<!--<Drawer />-->
	<div class="flex-1 flex flex-col" style="margin-top: 10px; margin-bottom: {height + 70}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div transition:slide class="flex items-start gap-2.5 mb-4">
					<!-- {#if message.role === 'assistant'}{/if} -->
					<div
						transition:scale
						class="
                     px-3 rounded-2xl {message.role === 'user'
							? ' max-w-[580px] ml-auto bg-slate-400 bg-opacity-50 '
							: ' max-w-[880px] mr-auto bg-gray-700 bg-opacity- shadow-xl shadow-primary-500/20'}
                            "
					>
						<div
							class={message.role === 'user'
								? 'text-sm font-normal py-2.5 text-gray-900 dark:text-white'
								: 'text-sm font-normal py-2.5 text-gray-900 opacity-100 dark:text-white'}
						>
							<!-- {@html marked.parse(decodeUnicode(message.content))} -->
							{@html marked.parse(
								decodeUnicode(formatLatexMath(message.content.replace(/\\n/g, '\n')))
							)}

							<!-- {@html marked.parse(decodeUnicode(processContent(message.content)))} -->
							<!-- {@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))} -->
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
	<div class="bottom-48"></div>
	<!-- <div class="bg-gradient-to-tr from-cyan-400 to indigo-400">yo soy the devil</div> -->

	<div class="fixed gap-2 inset-x-0 bottom-5 mx-4">
		<div
			class="max-w-4xl mx-auto rounded-3xl p-1 {isFocused
				? 'bg-gradient-to-bl from-tertiary-500/30 to-secondary-500/30'
				: ''}"
		>
			<div class=" bg-gray-800 rounded-3xl relative">
				<div class="flex flex-col w-full pr-14">
					<textarea
						{rows}
						on:resize={onResize}
						on:blur={onBlur}
						on:focus={onFocus}
						use:resize
						name="textareaContent"
						bind:this={textarea}
						placeholder="Send message to AI Tutor..."
						bind:value
						class="placeholder-secondary-700 flex-1 bg-transparent border-none outline-none min-h-[40px] max-h-[500px] text-white focus:ring-0"
					></textarea>

					<button
						on:click={() => {
							expandTextArea();
						}}
						class=" absolute top-1 right-1 max-h-14 px-2 py-2 text-white rounded-xl focus:bg-secondary-600"
					>
						{#if expanded}
							<SquareArrowDownLeft size="24" />
						{:else}
							<SquareArrowUpRight size="24" />
						{/if}
					</button>

					<button
						on:click={() => {
							sendMessage('user', textarea.value);
						}}
						class=" absolute bottom-2 right-2 max-h-14 px-2 py-2 bg-primary-500 text-black rounded-xl focus:bg-secondary-600"
						><SendHorizontal size="28" /></button
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
		transition: rows 550ms ease;
		overflow: hidden;
		overflow-y: scroll;
	}
</style>
