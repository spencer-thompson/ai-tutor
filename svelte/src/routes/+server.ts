// import {API_KEY} from '$env/static/private';
// import { jwt } from '$lib/stores/jwtStore';

export async function POST({ cookies }) {
    const token = cookies.get('token');
    console.log(token);
}

// import { jwt } from '$lib/stores/jwtStore';
//
// export function load({ cookies }) {
//     const token = cookies.get('token');
//
//     // const jwtkey = writable(jwt);
//     // console.log(jwt)
//     // console.log(jwtkey);
//
//     if (token) {
//         jwt.set(token);
//
//         jwt.subscribe(value => {
//             console.log('JWT value:', value);
//         })();
//     }
//
//     return {
//         authenticated: !!token,
//         token
//         // jwt: jwt === 'true'
//     };
// }



// export async function POST({ request }) {
//     const body = await request.json();
//     const { messages, courses } = body;
//
//     try {
//         // console.log(`JWT key: ${jwt}`);
//         // console.log(API_KEY);
//
//         const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
//             method: 'POST',
//         body: JSON.stringify({ messages, courses, model: 'gpt-4o' }),
//         headers: {
//             'Content-Type': 'application/json',
//             'AITUTOR-API-KEY': API_KEY,
//             Authorization: `Bearer ${jwt}`
//         }
//         });
//
//         return new Response(response.body, {
//             headers: {
//                 'Content-Type': 'text/event-stream',
//                 'Cache-Control': 'no-cache',
//                 'Connection': 'keep-alive'
//             }
//         });
//     } catch (error) {
//         return new Response(JSON.stringify({ success: false, error: error.message }), {
//             status: 500,
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         });
//     }
// }

// {
//     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDgxMDU3MCIsInVuaSI6InV2dSIsImV4cCI6MTczNzQ5MjE5NSwiaWF0IjoxNzM3NDA1Nzk1fQ.Q_S-6cpdp7p2hXxQAKCn9h0pqFBhw_BE-mJCSbjDtoU"
// }
//
//
// API_KEY=L52XnyeWj9PfPVZ5Uef8scMr0XgYYrQ0PNm1V6w0gvs



