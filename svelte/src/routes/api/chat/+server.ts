import {API_KEY} from '$env/static/private';
import { jwt } from '$lib/stores/jwtStore';


export async function POST({ request }) {
    const body = await request.json();
    const { messages, courses } = body;

    try {
        // console.log(`JWT key: ${jwt}`);
        // console.log(API_KEY);

        const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
            method: 'POST',
        body: JSON.stringify({ messages, courses, model: 'gpt-4o' }),
        headers: {
            'Content-Type': 'application/json',
            'AITUTOR-API-KEY': API_KEY,
            Authorization: `Bearer ${jwt}`
        }
        });

        return new Response(response.body, {
            headers: {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        });
    } catch (error) {
        return new Response(JSON.stringify({ success: false, error: error.message }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
}





	// function addMessage(role: Role, text: string) {
	// 	messages = [...messages, { role, content: text, name: 'Guts' }];
	// 	console.log(text);
	//
	// 	// console.log(import.meta.env.VITE_API_KEY);
	//
	// 	setTimeout(() => {
	// 		window.scrollTo(0, document.body.scrollHeight);
	// 	}, 0);
	// }

	// 	if (text.trim() != '') addMessage(role, value);
	// 	console.log(height);
	// 	console.log(inputHeight);
	// 	// console.log($jwt);
	// 	console.log(`${$jwt}`);
	// 	value = '';
	//
	// 	const courses = [101, 202];
	//
	// 	// let requestBody = {
	// 	// 	messages: messages,
	// 	// 	courses: courses
	// 	// };
	//
	// 	const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
	// 		method: 'POST',
	// 		body: JSON.stringify({
	// 			messages: messages,
	// 			courses: courses
	// 		}),
	// 		headers: {
	// 			'Content-Type': 'application/json',
	// 			'AITUTOR-API-KEY': `${import.meta.env.VITE_API_KEY}`,
	// 			Authorization: `Bearer ${$jwt}`
	// 		}
	// 	});
	// 	for await (const chunk of response.body) {
	// 		console.log(chunk);
	// 	}
	// }
