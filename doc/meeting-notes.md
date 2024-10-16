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
