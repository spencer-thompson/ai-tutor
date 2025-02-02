// import { jwt } from '$lib/stores/jwtStore';
import { API_KEY } from  '$env/static/private';
import type { Actions } from './$types';
import { API_KEY } from  '$env/static/private';


export function load({ cookies }) {
    const token = cookies.get('token');
    const apiKey = API_KEY;
       return {
        token,
        apiKey 
    };
}



