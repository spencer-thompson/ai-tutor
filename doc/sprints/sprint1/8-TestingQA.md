# Testing
- Testing Plan
  This testing plan outlines the strategy and procedures to ensure the AI Tutor application is reliable, functional, and secure. The plan covers multiple levels of testing, from individual components to the system as a whole.

  ### 1. Scope
  This plan applies to all components of the AI Tutor project, including:
  - **Backend:** The Python FastAPI application, including all API endpoints, business logic, and interactions with the database and external services (Canvas, LLMs).
  - **Frontend:** The Svelte-based web interface, including UI components, state management, and user interactions.
  - **Infrastructure:** The Docker-based containerization and deployment configuration.

  ### 2. Testing Strategy
  A multi-layered testing approach will be used to validate the application at different levels.

  #### a. Unit Testing
  - **Objective:** To verify that individual functions and components work correctly in isolation.
  - **Backend (Python):** Each function in the FastAPI application will have corresponding unit tests. Mocking will be used to isolate components from external dependencies like the database or the Canvas API.
    - **Tools:** `pytest`
  - **Frontend (Svelte):** Individual Svelte components and utility functions will be tested to ensure they render and behave as expected given specific props and user events.
    - **Tools:** `Vitest`, `Svelte Testing Library`

  #### b. Integration Testing
  - **Objective:** To verify that different parts of the application work together as intended.
  - **Backend:** Tests will focus on the interaction between API endpoints and the MongoDB database. For example, ensuring that creating a user via an endpoint correctly stores the user in the database.
    - **Tools:** `pytest`, `TestClient` for FastAPI
  - **Frontend-Backend:** Tests will verify that the frontend can successfully make API calls to the backend and handle the responses correctly. This will involve running both the frontend and backend servers in a test environment.
    - **Tools:** `Playwright` or `Cypress`

  #### c. End-to-End (E2E) Testing
  - **Objective:** To simulate real user scenarios from start to finish, ensuring the entire application flow is working correctly.
  - **Scenarios:** Key user journeys will be tested, such as:
    1.  User logs in via Canvas, asks a question in Smart Chat, and receives a context-aware answer.
    2.  User updates their bio, starts a new chat, and verifies the AI's tone has changed.
    3.  User asks a question that requires executing Python code.
  - **Tools:** `Playwright`

  #### d. Security Testing
  - **Objective:** To identify and mitigate potential security vulnerabilities.
  - **Methods:** 
    -   Regular dependency scanning to find known vulnerabilities in third-party packages.
    -   Manual penetration testing of key endpoints, focusing on authentication (JWT handling) and input validation to prevent injection attacks.
    -   Ensuring all sensitive data is handled securely and API keys are not exposed.

  ### 3. Roles and Responsibilities
  - **All Team Members:** Responsible for writing unit tests for the code they develop.
  - **Sprint Lead:** Responsible for overseeing the testing process, running integration and E2E tests before a release, and managing bug reports.

  ### 4. Metrics and Quality Assurance
  - **Code Coverage:** Aim for a minimum of 80% unit test coverage for the backend Python code, measured using `pytest-cov`.
  - **Bug Tracking:** All bugs will be logged as GitHub Issues. Each bug report will include a description, steps to reproduce, priority, and severity.
  - **Pass/Fail Criteria:** For a sprint to be considered complete, all unit and integration tests must pass, and there should be no outstanding critical or high-priority bugs.
- Test Cases
  This section provides a sample of test cases derived from the testing plan. The `Test Date` is set to the creation date and `Pass/Fail` status is pending execution.

  ### Unit Test Cases (Backend)

  | Test Case # | Description | Test Date | Inputs | Expected Outputs | Pass/Fail |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **UT-BE-01** | **User Model Validation:** Tests that the `User` Pydantic model in `models.py` successfully validates a correct user object. | 2025-10-05 | `{"sub": "123", "name": "Test User"}` | The `User` model is instantiated without errors. | Pending |
  | **UT-BE-02** | **Invalid User Model:** Tests that the `User` model raises a `ValidationError` if required fields are missing. | 2025-10-05 | `{"sub": "123"}` (missing `name`) | A `pydantic.ValidationError` is raised. | Pending |
  | **UT-BE-03** | **AI Response Formatting:** Tests a utility function in `ai.py` that formats a raw LLM response into the correct JSON structure for the frontend. | 2025-10-05 | Raw text string from a mocked LLM. | A valid JSON object with `type` and `content` fields is returned. | Pending |

  ### Unit Test Cases (Frontend)

  | Test Case # | Description | Test Date | Inputs | Expected Outputs | Pass/Fail |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **UT-FE-01** | **Message Component Rendering:** Verifies that the `Message.svelte` component correctly displays the message text and author. | 2025-10-05 | `props = { author: "AI", text: "Hello!" }` | The component renders a `div` containing the text "Hello!" and indicates it is from the "AI". | Pending |
  | **UT-FE-02** | **Send Button Event:** Verifies that clicking the "Send" button in the `ChatInput.svelte` component dispatches a `send` event. | 2025-10-05 | User clicks the send button. | A `send` event is dispatched with the input field's text content as the payload. | Pending |

  ### Integration Test Cases

  | Test Case # | Description | Test Date | Inputs | Expected Outputs | Pass/Fail |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **IT-BE-01** | **Get User Profile:** Verifies the `/api/users/me` endpoint. | 2025-10-05 | `GET` request to `/api/users/me` with a valid JWT for a user stored in the test database. | A `200 OK` response is returned with a JSON body containing the correct user's profile data. | Pending |
  | **IT-BE-02** | **Create Conversation:** Verifies the `/api/conversations/` endpoint. | 2025-10-05 | `POST` request to `/api/conversations/` with a valid JWT and a title. | A `201 Created` response is returned, and a new conversation document is created in the database for that user. | Pending |

  ### End-to-End Test Cases

  | Test Case # | Description | Test Date | Inputs | Expected Outputs | Pass/Fail |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **E2E-01** | **Full Login and Chat Flow:** Simulates a user logging in, sending a message, and receiving a response. | 2025-10-05 | 1. Navigate to home page. 2. Click "Login". 3. Complete mock Canvas login. 4. Type "Hello" into chat. 5. Click "Send". | 1. User is redirected to Canvas. 2. User is redirected back to the app. 3. The message "Hello" appears in the chat window. 4. An AI response is streamed into the chat window. | Pending |

  ### Security Test Cases

  | Test Case # | Description | Test Date | Inputs | Expected Outputs | Pass/Fail |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **ST-01** | **Unauthorized API Access:** Attempt to access an authenticated endpoint without proper credentials. | 2025-10-05 | `GET` request to `/api/users/me` with no `Authorization` header. | The API returns a `401 Unauthorized` or `403 Forbidden` status code. | Pending |
  | **ST-02** | **XSS in Chat Input:** Attempt to inject a script into the chat. | 2025-10-05 | User types `<script>alert('XSS')</script>` into the chat input and sends. | The message is displayed as plain text in the chat window, and no alert dialog appears. The script is sanitized. | Pending |

- Bug Report
  *This section will be populated with bug reports as they are identified during the testing process. At this time, formal testing has not yet begun.*

  | Date | Tester | Test Case Number | Priority | Severity Level | Assigned Developer | Fix Date |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | | | | | | | |

- Assessment Report
  *This section will contain an analysis of the testing results, including metrics trends and an overall assessment of application quality. This report will be generated after the initial testing cycles are complete.*

### 5. Preventive QA

- **Static Code Analysis:** Automated tools will be used to analyze the source code without executing it. This helps to identify potential vulnerabilities, bugs, and code smells early in the development process.
  - **Tools:** `ruff`, `bandit`
- **Code Reviews:** All new code will be reviewed by at least one other team member before it is merged into the main branch. This helps to ensure code quality, consistency, and knowledge sharing among the team.
- **Coding Standards:** The team will adhere to a consistent set of coding standards (e.g., PEP 8 for Python) to ensure that the codebase is readable and maintainable.

### 6. Design and Maintenance Metrics

#### a. Design Metrics
- **Cyclomatic Complexity:** This metric measures the complexity of a function's decision-making logic. A high cyclomatic complexity can indicate that a function is difficult to test and maintain. The target is to keep the cyclomatic complexity of all functions below 10.
- **Coupling:** This metric measures the degree of interdependence between modules. Low coupling is desirable, as it makes it easier to modify one module without affecting others.
- **Cohesion:** This metric measures how closely related the responsibilities of a single module are. High cohesion is desirable, as it indicates that a module has a well-defined purpose.

#### b. Maintenance Metrics
- **Mean Time To Repair (MTTR):** This metric measures the average time it takes to fix a bug, from the time it is reported to the time a fix is deployed. The target MTTR for critical bugs is less than 24 hours.
- **Mean Time Between Failures (MTBF):** This metric measures the average time between system failures. A high MTBF indicates a reliable system. The target MTBF is greater than 1000 hours.
- **Code Churn:** This metric measures the number of times a file is modified. A high code churn can indicate that a file is a "hotspot" in the codebase and may be a candidate for refactoring.