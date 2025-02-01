<script lang="ts">
	import { Avatar } from '@skeletonlabs/skeleton';
	import { marked } from 'marked';
	import { scale, slide } from 'svelte/transition';
	import { decodeUnicode } from '$lib/utils/markdown';

	export let message: Message;
</script>

<div transition:slide class="flex items-start gap-2.5 mb-4">
	{#if message.role === 'assistant'}
		<Avatar
			initials="UV"
			width="w-11"
			class="rounded-2xl"
			cursor="cursor-pointer"
			background="bg-primary-500"
		/>
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
			<!--{@html marked.parse(JSON.parse(`"${message.content}"`.replace(/\\n/g, '\n')))}-->
			{@html marked.parse(decodeUnicode(message.content.replace(/\\n/g, '\n')))}
			<!--{@html marked.parse(`"${message.content}"`.replace(/\\n/g, '\n'))}-->
			<!--{@html marked.parse(message.content)}-->
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
