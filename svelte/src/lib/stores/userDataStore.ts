import { writable } from 'svelte/store';

export const userData = writable({
    // You can provide default values here if needed
    // For example:
    // name: '',
    // role: '',
    // email: '',
    // preferences: {},
});

export function updateUserData(newData) {
        return {...newData };
}

