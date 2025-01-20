// import { writable } from 'svelte/store';
import { jwt } from '$lib/stores/jwtStore';

export function load({ cookies }) {
    const token = cookies.get('token');

    // const jwtkey = writable(jwt);
    // console.log(jwt)
    // console.log(jwtkey);

    if (token) {
        jwt.set(token);
        
        // jwt.subscribe(value => {
        //     console.log('JWT value:', value);
        // })();
    }

    return {
        authenticated: !!token,
        token
        // jwt: jwt === 'true'
    };
}



