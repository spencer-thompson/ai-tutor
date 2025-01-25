<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { marked } from 'marked';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';
	// import { enhance, applyAction } from '$app/forms';
	// import { onMount } from 'svelte';
	// import DOMPurify from 'dompurify';
	export let data;

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
		// { sender: role.user, message: 'this is a message from the user!' },
		// { sender: role.ai, message: marked.parse('# Marked in **the** *brower*') }
	];

	let buffer = '';
	let yBeforeSend: number;

	$: rows = (value.match(/\n/g) || []).length + 1 || 1;

	function scrolldown() {
		console.log(y);
		console.log(window.innerHeight);
		console.log(document.body.scrollHeight);

		if (document.body.scrollHeight - (window.innerHeight + y) < 30) {
			setTimeout(function () {
				window.scrollTo(0, document.body.scrollHeight);
				scrolldown();
			}, 0);
		}
	}

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
		readData();

		messages = [...messages, { role: 'assistant', content: '', name: 'ai' }];

		console.log(text);
	}

	async function sendMessage(role: string, text: string) {
		yBeforeSend = y;
		if (text.trim() != '') addMessage(role, text);

		scrolldown();

		console.log(height);
		console.log(inputHeight);
		console.log(data.token);
		console.log(data.apiKey);

		value = '';
		isLoading = true;
	}
</script>

<!-- document.cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNjkzNzkwIiwidW5pIjoidXZ1IiwiZXhwIjoxNzM3ODIxNjg3LCJpYXQiOjE3Mzc3MzUyODd9.XvSd8YEnWnEkCvgnCxppKcpdIJISHPTuk73nI92vJvE; expires=Fri, 30 Jan 2025 23:59:59 GMT; path=/"; -->

<!--style="margin-bottom: {120}px-->
<main class="flex flex-col min-h-screen">
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
		`${"Sure! Here's a simple example of markdown text:\n\nmarkdown\n# Welcome to Utah Valley University!\n\nUtah Valley University (UVU) is a public university located in **Orem, Utah**. It's an exciting place to learn, grow, and achieve your academic goals.\n\n## Why Choose UVU?\n\n- **Diverse Programs**: UVU offers a wide range of programs to suit your interests, from arts to sciences.\n- **Flexible Learning**: With both in-person and online classes, you can learn on your terms.\n- **Supportive Community**: UVU provides excellent resources to support students' success.\n\n## How to Apply\n\n1. Visit the [UVU Admissions](https://www.uvu.edu/admissions) page.\n2. Submit your application online.\n3. Send your transcripts and test scores.\n4. Await your acceptance letter!\n\n## Contact Us\n\nFor more information, feel free to reach out:\n\n- **Email**: info@uvu.edu\n- **Phone**: (801) 863-INFO\n\nJoin us at UVU, where your future begins!\n\n---\n\n> \Education is the most powerful weapon which you can use to change the world.\ \u2013 Nelson Mandela\n\n\nFeel free to use and modify this markdown to suit your needs! \ud83d\ude0a"}`
	)}
	<div class="flex-1 flex flex-col-reverse overflow-y-auto" style="margin-bottom: {height + 90}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div transition:slide class="flex items-start gap-2.5 mb-4">
					<div
						transition:scale
						class="
                    max-w-[620px] py-1 px-3 rounded-lg {message.role === 'user'
							? ' ml-auto bg-blue-600 rounded-br-none'
							: ' mr-auto bg-gray-300 rounded-bl-none'}
                            "
					>
						<p
							class={message.role === 'user'
								? 'text-sm font-normal py-2.5 text-gray-900 dark:text-white'
								: 'text-sm font-normal py-2.5 text-gray-900 dark:text-black'}
						>
							{@html marked.parse(message.content)}
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

<svelte:window bind:scrollY={y} />

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
