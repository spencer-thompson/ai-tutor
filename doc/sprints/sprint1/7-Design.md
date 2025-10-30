# Design
- Class Diagram (High Cohesion and Loose Coupling)
  ![Class Diagram](./assets/classdiagram.png)
- Design patterns
    -   **Singleton Pattern:** The FastAPI application instance (`app`) and the MongoDB client (`app.mongodb_client`) are initialized once and used throughout the application's lifecycle. This is managed by the `db_lifespan` async context manager, ensuring a single, shared connection to the database.
    -   **Strategy Pattern:** The backend can use different large language models (e.g., OpenAI, Anthropic) to generate responses. The `openai_iter_response` and `anthropic_iter_response` functions in `ai.py` represent different strategies for the same task. The application can select the strategy based on the user's choice of model.
    -   **Decorator Pattern:** The FastAPI framework uses decorators extensively to define API endpoints (e.g., `@app.get`, `@app.post`). These decorators add routing and other functionality to the endpoint functions without modifying their core logic, which is a clear example of the Decorator pattern.
- Architecture diagram
  ![Architecture Diagram](./assets/archdiagram.png)
- ERD diagram
  ![ERD Diagram](./assets/erddiagram.png)
- Use case diagram
  ![Use Case Diagram](./assets/usecasediagram.png)


### Use Case Descriptions

*   **Authenticate with UVU ID:** The user logs into the system. The system initiates an OAuth2 flow with the external Canvas LMS, which handles the actual authentication using the user's UVU credentials.
*   **Fetch User Profile:** The user retrieves their current profile information from the system, such as their name and custom bio, which is then displayed in the application's settings interface.
*   **Update User Profile:** The user modifies and saves their profile information (specifically their bio) to personalize the AI's tone and responses.
*   **List Conversations:** The user's client application requests and displays a list of all their past chat sessions, allowing them to select a previous conversation for review.
*   **Retrieve Conversation:** After a user selects a conversation from the list, the client application retrieves the full message history for that specific chat session from the server.
*   **Initiate Smart Chat:** The user starts a new conversation in "smart chat" mode. This is a distinct action that tells the backend to inject context from the user's Canvas data into the AI's prompt.
*   **Send Chat Message:** The user sends a query to the AI Tutor. This is the most common action. This use case can be extended with specialized tools if the query requires them.
*   **Access Course Info:** When a "Smart Chat" is active, the system automatically fetches the user's course information, assignments, and other relevant data from the Canvas API to provide context for the AI's response. This is a system action triggered by the user's chat message.
*   **Fetch Web Content:** As an extension of "Send Chat Message," if the user's query contains a URL, the AI can use this tool to access the content of that webpage to inform its answer.
*   **Execute Python Code:** As an extension of "Send Chat Message," the AI can use this tool to write and run Python code in a secure, sandboxed environment to perform calculations, run algorithms, or demonstrate programming concepts.
*   **View System Analytics:** The Administrator accesses a separate analytics dashboard (Plausible) to view aggregated, anonymized usage data and system performance metrics.
