<script lang="ts">
	import { SendHorizontal } from 'lucide-svelte';
	import { resize } from '$lib/components/textarea/resize';

	export let onSend: (text: string) => void;

	let textarea: HTMLTextAreaElement;
	let height = 120;
	let value = '';

	function onResize(event) {
		const { detail } = event;
		if (detail.CR) {
			textarea = event.target;
			height = event.detail.CR.height;
		}
	}

	$: rows = (value.match(/\n/g) || []).lenght + 1 || 1;
</script>

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
