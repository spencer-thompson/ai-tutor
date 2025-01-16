// import { writable } from 'svelte/store';
import {jwt } from '$lib/stores/jwtStore';

export function load({ cookies }) {
    const token = cookies.get('token');

    // const jwtkey = writable(jwt);
    console.log(jwt)
    // console.log(jwtkey);
    // if (token) {
    //     jwt.set(token);
    // }

    return {
        // authenticated: !!token,
        // token
        jwt: jwt === 'true'
    };
}
