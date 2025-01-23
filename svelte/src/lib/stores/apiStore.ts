import { writable } from 'svelte/store';

export const api = writable<string | null>(null);
