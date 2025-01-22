import { API_KEY } from  '$env/static/private';

    //
    // export async ({ cookies, request }) => {
    //     console.log("hello there");
    //
    //     const data = await request.formData();
    //     const content = data.get('textareaContent');
    //     const token = (cookies.get('token'));
    //     console.log(cookies.get('token'));
    //     console.log(API_KEY);
    //     console.log(content);
    //     console.log(data.get('textareaContent'));
    //     const payload = {
    //         messages: [
    //             {
    //                 name: "Joshua", 
    //                 role: "user",
    //                 content: content
    //             }
    //         ],
    //         courses: [101, 202], 
    //         model: "gpt-4o"
    //     };
    //     // console.log(JSON.stringify(payload));
    //     // console.log(payload);
    //
    //     try {
    //         // Make the POST request
    //         const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'AITUTOR-API-KEY': API_KEY,
    //                 'Authorization': `Bearer ${token}`
    //             },
    //             body: JSON.stringify(payload)
    //         });
    //
    //         // const decoder = new TextDecoder();
    //
    //         for await (const chunk of response.body) {
    //             console.log(chunk);
    //             // console.log(chunk.toBase64({ omitPadding: true}));
    //
    //         }
