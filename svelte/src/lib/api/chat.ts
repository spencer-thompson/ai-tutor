export async function streamChat(messagages: Message[], apiKey, string, token: string) {
    const payload = {
        messages,
        courses: [101, 202],
        model: 'gpt-4o'
    };

    const response = await fetch('https://api.aitutor.live/v1/smart_chat_stream', {
        method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'AITUTOR-API-KEY': apiKey,
        Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
    });

    return response;
}
