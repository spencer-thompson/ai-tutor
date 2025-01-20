<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';
	import { marked } from 'marked';
	import { jwt } from '$lib/stores/jwtStore';
	import { blur, crossfade, draw, fade, fly, scale, slide } from 'svelte/transition';

	export let data;

	$: if (data.token) {
		$jwt = data.token;
	}

	let name = 'textarea',
		textarea = '',
		height = 120,
		value = ``,
		inputHeight = 0;

	let chatContainer;

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

	enum Role {
		user,
		ai
	}

	interface Message {
		role: Role;
		content: string;
		name: string;
	}

	let messages: Message[] = [
		// { sender: role.user, message: 'this is a message from the user!' },
		// { sender: role.ai, message: marked.parse('# Marked in **the** *brower*') }
	];

	function addMessage(role: Role, text: string) {
		messages = [...messages, { role, content: text, name: 'Guts' }];
		console.log(text);

		console.log(import.meta.env.VITE_API_KEY);

		setTimeout(() => {
			window.scrollTo(0, document.body.scrollHeight);
		}, 0);
	}

	async function sendMessage(role: Role, text: string) {
		if (text.trim() != '') addMessage(role, value);
		console.log(height);
		console.log(inputHeight);
		// console.log($jwt);
		console.log(`${$jwt}`);
		value = '';

		const courses = [101, 202];

		// let requestBody = {
		// 	messages: messages,
		// 	courses: courses
		// };

		const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
			method: 'POST',
			body: JSON.stringify({
				messages: messages,
				courses: courses
			}),
			headers: {
				'Content-Type': 'application/json',
				'AITUTOR-API-KEY': `${import.meta.env.VITE_API_KEY}`,
				Authorization: `Bearer ${$jwt}`
			}
		});
		for await (const chunk of response.body) {
			console.log(chunk);
		}
	}
</script>

<!--style="margin-bottom: {120}px-->
<main class="flex flex-col min-h-screen overflow-y-auto">
	<div class="flex-1 flex flex-col-reverse" style="margin-bottom: {height + 90}px">
		<div transition:fade class="w-full max-w-4xl mx-auto px-4">
			{#each messages as message}
				<div transition:slide class="flex items-start gap-2.5 mb-4">
					<div
						transition:scale
						class="
                    max-w-[220px] py-1 px-3 rounded-lg {message.role === Role.user
							? ' ml-auto bg-blue-600 rounded-br-none'
							: ' mr-auto bg-gray-300 rounded-bl-none'}
                            "
					>
						<p
							class={message.role === Role.user
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
						on:click={() => sendMessage(Role.user, textarea.value)}
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
		will-change: height;
		transition: rows 250ms ease;
		overflow: hidden;
		/* overflow-x: scroll; */
	}
</style>
