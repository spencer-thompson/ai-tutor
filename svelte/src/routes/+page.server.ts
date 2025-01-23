// import { jwt } from '$lib/stores/jwtStore';
import { API_KEY } from  '$env/static/private';
import type { Actions } from './$types';
import { API_KEY } from  '$env/static/private';


export function load({ cookies }) {
    const token = cookies.get('token');
    const apiKey = API_KEY;
    
    // if (token) {
    //     jwt.set(token);
    //     api.set(String(API_KEY));
    //
    //     jwt.subscribe(value => {
    //         console.log('JWT value:', value);
    //     })();
    //
    //     api.subscribe(value => {
    //         console.log('API KEY value:', value);
    //     })();
    //
    // }

    return {
        token,
        apiKey 
    };
}

export const actions: Actions = {
    send: async ({ cookies, request }) => {
        console.log("hello there");

        const data = await request.formData();
        const content = data.get('textareaContent');
        const token = (cookies.get('token'));
        console.log(cookies.get('token'));
        console.log(API_KEY);
        console.log(content);
        console.log(data.get('textareaContent'));
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
        // console.log(JSON.stringify(payload));
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
            }).then((response) => {
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                return new ReadableStream({
                    start(controller) {
                        return pump();
                        function pump() {
                            return reader.read().then(({done, value }) => {
                                const json = JSON.parse(decoder.decode(value));
                                console.log(json.content);
                                if (done) {
                                    controller.close();
                                    return;
                                }
                                controller.enqueue(value);
                                return pump();
                            });
                        }
                    },
                });
            });
        
            // const decoder = new TextDecoder();

            // for await (const chunk of response.body) {
            //     console.log(chunk);
                // console.log(chunk.toBase64({ omitPadding: true}));


            // const reader = response.body.getReader();
            // const decoder = new TextDecoder();
            //
            //
            // let result = '';
            // while (true) {
            //     const { done, value } = await reader.read();
            //
            //     if (done) break;
            //     console.log(decoder.decode(value, {stream: true }));
            //     result += decoder.decode(value, { stream: true });
            // }
            // console.log('Stream contents:', result);



            //
            // return new Response(response.body, {
            //     headers: {
            //         'content-Type': 'text/event-stream',
            //         'Cache-Control': 'no-cache',
            //         'Connection': 'keep-alive'
            //     }
            // });

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





