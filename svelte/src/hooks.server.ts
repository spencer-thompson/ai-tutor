import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    event.locals.buffer = ''; // Initialize buffer in locals
    const response = await resolve(event);
    return response;
};
