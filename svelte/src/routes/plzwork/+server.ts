
import { API_KEY } from '$env/static/private';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ cookies, request }) => {
    try {
        console.log("Request received!");

        // Parse JSON request body
        const data = await request.json();
        const content = data.textareaContent;
        const token = cookies.get('token');

        // Log all relevant information
        console.log("Token:", token);
        console.log("API_KEY:", API_KEY);
        console.log("Content:", content);
        console.log("Full Request Data:", data);


        if (!content) {
            console.error("No content provided!");
            return new Response('Content cannot be empty', { status: 400 });
        }

        // If everything is fine, respond with success
        return new Response('Data logged successfully', { status: 200 });
    } catch (error) {
        // Log the error with details
        console.error("Error processing request:", error);
        return new Response('Internal Server Error', { status: 500 });
    }
};

