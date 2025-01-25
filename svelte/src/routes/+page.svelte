<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { marked } from 'marked';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';
	// import { enhance, applyAction } from '$app/forms';
	// import { onMount } from 'svelte';
	// import DOMPurify from 'dompurify';
	import { clipboard, Avatar } from '@skeletonlabs/skeleton';

	export let data;

	marked.setOptions({
		breaks: true,
		gfm: true
	});

	let y: number;

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

	interface Message {
		role: string;
		content: string;
		name: string;
	}

	let messages: Message[] = [
		{ role: 'user', content: 'this is a message from the user!', name: 'Guts' },
		{ role: 'assistant', content: marked.parse('# Marked in **the** *browser*'), name: 'ai' }
	];

	let buffer = '';

	$: rows = (value.match(/\n/g) || []).length + 1 || 1;

	function scrolldown() {
		if (document.body.scrollHeight - (window.innerHeight + y) < 30) {
			setTimeout(function () {
				window.scrollTo(0, document.body.scrollHeight);
				scrolldown();
			}, 0);
		}
	}

	function copyHandler(message: string) {
		console.log(message);
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
	}

	function addMessage(role: string, text: string) {
		messages = [...messages, { role, content: text, name: 'Joshua' }];
		readData();

		messages = [...messages, { role: 'assistant', content: '', name: 'ai' }];

		console.log(text);
	}

	async function sendMessage(role: string, text: string) {
		if (text.trim() != '') addMessage(role, text);

		scrolldown();
		value = '';
		isLoading = true;
	}
</script>

<!-- document.cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNjkzNzkwIiwidW5pIjoidXZ1IiwiZXhwIjoxNzM3OTMyMTE1LCJpYXQiOjE3Mzc4NDU3MTV9.mGDOUzbNsQaZiWJWcpcpwABHqI-8z2z6iQOzkfZsoNc; expires=Fri, 30 Jan 2025 23:59:59 GMT; path=/"; -->

<!--style="margin-bottom: {120}px-->
<main class="flex flex-col min-h-screen">
	{@html marked.parse(
		"Absolutely! Here's a basic example of Markdown to get you started:\n\nmarkdown\n# Heading 1\n\n## Heading 2\n\n### Heading 3\n\n**Bold Text**\n\n*Italic Text*\n\n- Bullet Point 1\n- Bullet Point 2\n - Nested Bullet Point\n\n1. Numbered List Item 1\n2. Numbered List Item 2\n\n[Link to UVU](https://www.uvu.edu)\n\n![Image Alt Text](https://www.uvu.edu/logo.png)\n\n> Blockquote\n\n`Inline code`\n\n\nCode block\n\n\n\nFeel free to ask if you have any more questions or need further assistance! \ud83d\ude0a"
	)}
	<pre>The quick brown fox jumps over the lazy dog.</pre>
	Press<kbd>⌘ + C</kbd> to copy.
	<del><s>Always</s> Gonna Give You Up</del>
	<ins cite="https://youtu.be/dQw4w9WgXcQ" datetime="10-31-2022"> Never Gonna Give You Up </ins>
	{@html marked(
		`${`Marked - Markdown Parser
========================

[Marked] lets you convert [Markdown] into HTML.  Markdown is a simple text format whose goal is to be very easy to read and write, even when not converted to HTML.  This demo page will let you type anything you like and see how it gets converted.  Live.  No more waiting around.

How To Use The Demo
-------------------

1. Type in stuff on the left.
2. See the live updates on the right.

That's it.  Pretty simple.  There's also a drop-down option above to switch between various views:

- **Preview:**  A live display of the generated HTML as it would render in a browser.
- **HTML Source:**  The generated HTML before your browser makes it pretty.
- **Lexer Data:**  What [marked] uses internally, in case you like gory stuff like this.
- **Quick Reference:**  A brief run-down of how to format things using markdown.

Why Markdown?
-------------

It's easy.  It's not overly bloated, unlike HTML.  Also, as the creator of [markdown] says,

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

Ready to start writing?  Either start changing stuff on the left or
[clear everything](/demo/?text=) with a simple click.

[Marked]: https://github.com/markedjs/marked/
[Markdown]: http://daringfireball.net/projects/markdown/`}`
	)}
	{@html marked(
		`${"\ud83d\ude04 Sure! Here's a simple example of markdown text:\n\nmarkdown\n# Welcome to Utah Valley University!\n\nUtah Valley University (UVU) is a public university located in **Orem, Utah**. It's an exciting place to learn, grow, and achieve your academic goals.\n\n## Why Choose UVU?\n\n- **Diverse Programs**: UVU offers a wide range of programs to suit your interests, from arts to sciences.\n- **Flexible Learning**: With both in-person and online classes, you can learn on your terms.\n- **Supportive Community**: UVU provides excellent resources to support students' success.\n\n## How to Apply\n\n1. Visit the [UVU Admissions](https://www.uvu.edu/admissions) page.\n2. Submit your application online.\n3. Send your transcripts and test scores.\n4. Await your acceptance letter!\n\n## Contact Us\n\nFor more information, feel free to reach out:\n\n- **Email**: info@uvu.edu\n- **Phone**: (801) 863-INFO\n\nJoin us at UVU, where your future begins!\n\n---\n\n> \Education is the most powerful weapon which you can use to change the world.\ \u2013 Nelson Mandela\n\n\nFeel free to use and modify this markdown to suit your needs! \ud83d\ude0a"}`
	)}
	<div class="flex-1 flex flex-col-reverse overflow-y-auto" style="margin-bottom: {height + 90}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div transition:slide class="flex items-start gap-2.5 mb-4">
					<!--<button class="px-2" use:clipboard={message.content}>Copy</button>-->
					{#if message.role === 'assistant'}
						<button
							on:click={() => {
								copyHandler(message.content);
							}}
						>
							<Avatar
								initials="UV"
								width="w-11"
								class="rounded-2xl"
								cursor="cursor-pointer"
								background="bg-primary-500"
							/>
						</button>
					{/if}
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
							{@html marked.parse(message.content.replace(/\\n/g, '\n'))}
							<!--{@html message.content}-->
						</p>
					</div>
					{#if message.role === 'user'}
						<button
							on:click={() => {
								console.log(message.content);
							}}
						>
							<Avatar initials="JD" width="w-11" class="rounded-2xl" background="bg-red-700" />
						</button>
					{/if}
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
