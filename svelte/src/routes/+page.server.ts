import type { Actions } from './$types';
import { API_KEY } from  '$env/static/private';

export const actions: Actions = {
    send: async ({ cookies, request }) => {
        console.log("hello there");

        const data = await request.formData();
        const content = data.get('textareaContent');
        const token = (cookies.get('token'));
        console.log(cookies.get('token'));
        console.log(API_KEY);
        console.log(content);
        const payload = {
            messages: [
                {
                    name: "Joshua", 
                    role: "user",
                    content: content
                }
            ],
            courses: [101, 202], 
            model: "gpt-4o"
        };
        console.log(JSON.stringify(payload));
        // console.log(payload);

        try {
            // Make the POST request
            const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'AITUTOR-API-KEY': API_KEY,
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });


            console.log(response.body);
    //
    //         if (!response.ok) {
    //             const errorText = await response.text();
    //             console.error("Error from API:", {
    //                 status: response.status,
    //                 statusText: response.statusText,
    //                 body: errorText
    //             });
    //             return {
    //                 success: false,
    //                 error: `API Error: ${response.status} ${response.statusText}`
    //             };
    //         }
    //
    //         // Handle the streaming response
    //         const reader = response.body?.getReader();
    //         if (!reader) {
    //             throw new Error('No readable stream available');
    //         }
    //
    //         // Return a readable stream that can be consumed by the client
    //         return {
    //             success: true,
    //             stream: new ReadableStream({
    //                 async start(controller) {
    //                     try {
    //                         while (true) {
    //                             const { done, value } = await reader.read();
    //                             if (done) {
    //                                 controller.close();
    //                                 break;
    //                             }
    //                             controller.enqueue(value);
    //                         }
    //                     } catch (error) {
    //                         controller.error(error);
    //                     }
    //                 }
    //             })
    //         };
        } catch (error) {
            console.error("Error during API call:", error);
            return {
                success: false,
                error: "Failed to connect to AI Tutor API"
            };
        }
    }
}



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



// import { jwt } from '$lib/stores/jwtStore';
//
// export function load({ cookies }) {
//     const token = cookies.get('token');
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
//     };
// }




