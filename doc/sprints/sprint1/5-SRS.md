# Software Requirement Specification (SRS)

## Functional Requirements

### User Management
- **F1.1:** Users must be able to log in to the system using their UVU credentials via Canvas OAuth2.
- **F1.2:** The system must use JSON Web Tokens (JWT) for authenticating API requests after the initial login.
- **F1.3:** Users shall be able to set a custom bio in their profile. The content of this bio will be included in the system prompt sent to the AI to influence its responses.
- **F1.4:** The system shall provide an administrative dashboard that displays the following real-time analytics: total number of users, number of active users, and total messages sent.

### Chat Interface
- **F2.1:** The system shall provide a web-based chat interface for users to interact with the AI Tutor.
- **F2.2:** The chat interface must display the conversation history, with user and AI messages clearly distinguished.
- **F2.3:** The system shall stream messages to the client in real-time using websockets or a similar technology.
- **F2.4:** The chat interface shall render AI responses in GitHub-flavored markdown, supporting tables, lists, bold, italics, and other standard formatting.
- **F2.5:** The system must render mathematical equations formatted using LaTeX syntax.
- **F2.6:** The system must provide syntax highlighting for code snippets in Python, JavaScript, Java, C++, and SQL.

### AI Tutor
- **F3.1:** The AI Tutor shall generate responses to user queries using a large language model (LLM) specified in the system configuration (e.g., GPT-4, Claude 3).
- **F3.3:** The system shall provide a "smart chat" feature that injects context from the user's Canvas data into the LLM prompt to generate personalized responses.
- **F3.4:** The AI Tutor shall be able to retrieve the user's enrolled courses, upcoming assignments, and recent grades from the Canvas API.
- **F3.5:** The AI Tutor shall have the ability to use the following tools to perform specific tasks:
    - **F3.5.1:** A web scraper tool that can read the full text content of a webpage given a URL.
    - **F3.5.2:** A Python code interpreter that can execute sandboxed Python code to perform calculations or demonstrate programming concepts.
- **F3.6:** All user input and AI-generated responses must be passed through a content moderation filter. Any content flagged as inappropriate (e.g., hate speech, violence) shall be blocked and logged.

## Non-functional Requirements

### Security
- **NF1.1:** All network communication between the client and server must be encrypted using TLS 1.2 or higher.
- **NF1.2:** The system must be protected against the OWASP Top 10 web vulnerabilities, which includes Cross-Site Scripting (XSS) and NoSQL Injection.
- **NF1.3:** Access to the backend API must be restricted to authenticated users with valid JWTs. Direct access via API keys is prohibited.
- **NF1.4:** All user data, including Canvas information and chat history, must be encrypted at rest in the database using AES-256 encryption.

### Performance
- **NF2.1:** The user interface shall have a response time of less than 200ms for all user interactions (e.g., button clicks, page loads).
- **NF2.2:** The first token of a streamed AI response shall be delivered to the client in under 2 seconds, on average.
- **NF2.3:** The system shall initially support 100 concurrent users with an average API response time of under 500ms.

### Usability
- **NF3.1:** A new user must be able to successfully send a message in "smart chat" mode within 60 seconds of their first login without requiring documentation.
- **NF3.2:** All error messages displayed to the user must include a unique error code and a clear, human-readable explanation of the problem.
- **NF3.3:** The AI Tutor's responses shall achieve a Flesch-Kincaid grade level score between 8 and 12 to ensure they are understandable to a broad audience.

### Scalability
- **NF4.1:** The system shall be horizontally scalable. An increase in container instances must result in a proportional increase in user capacity.
- **NF4.2:** The application shall be fully containerized using Docker, with all services defined in a `docker-compose.yml` file for automated deployment and scaling.

### Reliability
- **NF5.1:** The system shall have a service availability of 99.9% (uptime).
- **NF5.2:** The system shall have a Mean Time To Recovery (MTTR) of less than 15 minutes.
- **NF5.3:** The content moderation filter shall have a false negative rate of less than 1% for clearly inappropriate content.

### Maintainability
- **NF6.1:** All Python code must adhere to the PEP 8 style guide, enforced by an automated linter.
- **NF6.2:** The application shall have a modular design, with a clear separation of concerns between the data, business logic, and presentation layers.
- **NF6.3:** All new code committed to the main branch must have a minimum of 80% unit test coverage.
