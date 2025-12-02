# Project Description

The AI Tutor is a generative AI-powered learning assistant designed to support students at Utah Valley University (UVU). It provides a personalized and interactive learning experience by integrating with the Canvas Learning Management System (LMS). The application consists of a web-based frontend and a robust backend, working together to deliver a seamless and intuitive user experience.

The frontend is a modern chat interface built with Svelte. It allows students to ask questions and receive answers from an AI tutor in a conversational manner. The interface supports rich text formatting, including markdown, code snippets with syntax highlighting, and mathematical equations using LaTeX. This ensures that the AI can provide clear and easy-to-understand explanations for a wide range of subjects.

The backend is the core of the AI Tutor, developed using Python and the FastAPI framework. It orchestrates the entire system, managing user authentication, data processing, and communication with external services. The backend uses a MongoDB database to store user data, chat history, and course information.

One of the key features of the AI Tutor is its "smart chat" functionality. By securely accessing a student's data from Canvas—including their enrolled courses, assignments, grades, and activity stream—the AI can provide context-aware and personalized assistance. For example, a student can ask for a summary of their upcoming assignments, clarification on a specific course topic, or help with a difficult concept from a lecture. The AI can also be customized by the user with a bio, to further personalize the experience.

To answer a wide range of questions, the AI Tutor is equipped with several tools. It can read the content of webpages, which is useful for providing explanations based on external resources. It can also execute Python code, allowing it to function as a calculator or to demonstrate programming concepts.

The AI Tutor is designed to be a safe and reliable learning environment. It includes a moderation service that filters out inappropriate content, and it uses a secure authentication system based on JSON Web Tokens (JWT) to protect user data. The application is also designed to be scalable and maintainable, with a containerized architecture using Docker.

In summary, the AI Tutor is a comprehensive and innovative learning platform that combines the power of generative AI with the rich data available in the Canvas LMS. It aims to provide UVU students with a powerful and accessible tool to enhance their learning experience and academic success.
