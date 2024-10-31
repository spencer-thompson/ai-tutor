# Meeting Notes - October 11th, 2024  
**Time:** 12:00pm – 1:00pm  

## Meeting Objectives  
- **Define and finalize the project's goal and mission statement**  
  - Create an AI tutor accessible for Technology Management students.
  - Enhance learning through innovative technologies.

- **Establish clear communication and reporting practices**  
  - One-on-one meetings after the main session to create tasks.
  - Mid-week calls to assess progress.

- **Ensure all team members are on GitHub**  
  - Add members to Git and introduce GitHub Issues for task management.
  - Demo the process.

- **Discuss the feasibility of a mobile app version of the AI Tutor**

- **Evaluate feasibility of a web application or UVU access token**  
  - Choose the route (Mobile app or Browser extension for UVU students).

## Feature Discussions  
### Pros and Cons Evaluation  
**Mobile App Using Personal Token**  
| Pros                          | Cons                |
|-------------------------------|---------------------|
| Larger user base beyond UVU   | Access token blocked|

### Roadblocks  
- **Full integration with UVU Canvas**
  - Challenges for data access and integration.

### New Ideas  
- **Web Browser Extension**  
  - Create a better Canvas integration experience.
  - Real-time voice API to facilitate interactive tutoring.

- **Other Options**  
  - Allow departments to purchase the tutor for their students.
  - Discuss user login options:
    - Use Canvas to log in.
    - Create separate user accounts.

- **Flow Diagram**  
  - Map out how the extension works, including information retrieval for each class.
  - Choose a browser extension to demo for Dr. Thackery and the Dean of Engineering.

### Chosen Approach  
- **Backend Development**
  - Create a backend Docker container.
  - Communicate between backend and frontend.
  - Populate a MongoDB database.
- **Research & Learning**
  - Research tools to extend Chrome capabilities.
  - Learn Flutter for UI development.
  - Define the database structure.

## Milestones for Mobile App  
- Define the database schema and data points needed from the browser extension.
- Create user login capability.
- Pull data from the browser extension.
- Develop the Flutter app chat feature for mobile.
- Connect the app to the tutor backend.
- Upload to the browser extension store.

## Task List
### Browser Extension  
- Develop Flutter chat AI.
- Integrate UI with the extension.
- Create a new subdomain for the AI tutor.

### Flutter App  
- Transfer to Neonvim.
- Develop Chat UI display.

## Feature List  
### Mobile App  
- Chat interface.
- User login.
- Saved and unsaved chats.
- Communication with browser extension.

### Browser Extension  
- Pulling live data from Canvas.
- Maintaining functionality while the browser is open.

## Scope and Deliverables  
- **Deliverables**: Mobile app and browser extension.
- **Scope**:  
  - Develop a chat interface customized for university use with Canvas LMS via a browser extension.
  - Potential for a live voice interaction feature.
  - Implement new features to pull live data from Canvas using a crowdsourcing approach.
 
---

# Meeting Notes - October 25th 2024

## Topics Discussed

### Apache Airflow
- Asmaa mentioned that **Apache Airflow** is a tool to assist with the data pipeline.

### MongoDB
- There are **3 collections** in MongoDB related to the project.

## Plan for the Week
- Asmaa reiterated that **Apache Airflow** will be crucial for the data pipeline.

### Key Milestone
- By **Friday, November 8th**, we aim to have:
  - A **working system**.
  - A **browser extension**.
  - A **working app**.
  - **Airflow** fully functional.

## Demo Planning
- Schedule a demo for the **second week of December**.
- Identify **1 to 3 use cases** to showcase during the demonstration.
- Explore the possibility of adapting this into **different learning systems** in the future.
- Include a demonstration of the **mobile app**.

## User Types and Requirements
- **Developer**: Needs for building and maintaining the system.
- **Students**: Interface and data necessary for learning purposes.
- **Teacher**: Insights required to effectively help their students.
- **Researcher**: Types of data needed for research analysis.

## Risks
- **Data Latency**: Time for data to be processed and appear on the mobile app.
- **User Experience**: Potential issues with users needing to download multiple apps.

