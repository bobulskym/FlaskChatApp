# Chat App with Flask, WebSockets, and Azure Deployment

This is a real-time chat application built with Python, Flask, and WebSockets, leveraging Flask-SocketIO for instant message delivery. The app is containerized using Docker and designed for deployment on platforms like Azure App Service and Azure Storage Static Websites.

## Features
- User Authentication: Register and log in with secure password hashing and JWT authentication.
- Real-time Messaging: Chat updates instantly using WebSockets.
- Frontend & Backend Separation:
  - Backend: REST API with WebSocket support.
  - Frontend: Simple HTML, CSS, and JavaScript.
- Persistent Chat History: Messages and users are stored in CSV files.
- Scalable Deployment: Dockerized backend and lightweight frontend for flexibility.

## Technologies Used
- Python:
  - Flask for API and backend logic.
  - Flask-SocketIO for WebSockets.
  - Flask-CORS for handling cross-origin requests.
  - PyJWT for secure JSON Web Tokens.
  - Eventlet for WebSocket server support.
- Frontend:
  - HTML, CSS, and JavaScript (no frameworks for simplicity).
  - Fetch API for REST calls.
  - Socket.IO for WebSocket communication.
- Docker:
  - Containerized the backend for easy deployment.
- Azure:
  - Azure Container Registry: Hosting the backend API.
  - Azure App Service: Running the backend Docker container.
  - Azure Storage Static Website: Hosting the frontend.

## How It Works
1. Authentication:
   - Users register with a nickname and password.
   - Login generates a JWT token, stored in localStorage for subsequent requests.
   - All API requests and WebSocket communications are authenticated using the JWT.

2. Messaging:
   - Users send messages via WebSocket.
   - Backend broadcasts messages to all connected users.
   - Chat history is stored in a CSV file and loaded when users join the app.

3. Frontend:
   - Hosted as a static website (e.g., Azure Storage Static Website).
   - Communicates with the backend using REST API (for login and loading history) and WebSockets (for real-time updates).

4. Backend:
   - REST API endpoints for user management and chat operations.
   - WebSocket server handles real-time messaging.
   - Deployed as a Docker container (e.g., Azure App Service).

## Deployment

### Backend Deployment
The backend API is containerized and can be deployed to Azure Container Registry or any Docker-compatible service.

Steps:
1. Build Docker Image:
docker build -t flask-chat-api .


2. Deploy to Azure App Service:
- Push Docker image into an Azure Container Registry
- Create an Azure App Service using the container image.
- Ensure CORS is configured properly if your frontend is hosted elsewhere.

### Frontend Deployment
The frontend is a collection of static files that need to be deployed separately.

Steps:
1. Replace Backend API URLs:
Update `index.html` and `chat.html` and replace all `http://0.0.0.0:5000` URLs with your deployed backend API URL (e.g., `https://your-backend.azurewebsites.net`).

2. Deploy to Azure Static Website:
- Enable Static Website Hosting in Azure Storage Container (Creates a $web folder).
- Upload the `index.html`, `chat.html`, and `style.css` files.

## Example Usage

1. Open the Frontend:
Visit your Azure Static Website (e.g., `https://your-frontend-url`).

2. Register/Login:
- Register a new user with a nickname and password.
- Login to generate a JWT token.

3. Chat in Real-Time:
- Send messages, and see them update instantly across all connected clients.
- Clear chat history

4. Logout:
Click the logout button to return to the login page.

## Future Improvements
- Replace CSV storage with a database (e.g., SQLite, PostgreSQL).
- Add admin features for managing users and chat history.
- Improve UI with more advanced styling or frameworks (e.g., React).
- Enhance security (e.g., rate-limiting, password complexity checks).
