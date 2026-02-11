# AI Chat Agent System

This is a complete AI chat agent system with a FastAPI backend and Streamlit frontend with n8n workflow.

## System Architecture

The system follows this data flow:
1. **Frontend** → Sends chat messages to **Backend**
2. **Backend** → Forwards messages to **n8n Workflow** via webhook
3. **n8n Workflow** → Processes the message and returns response
4. **Backend** → Forwards response back to **Frontend**

## Prerequisites

- Python 3.7+
- pip
- An active n8n workflow with the webhook endpoint configured
- The n8n workflow must be running and accessible at the URL specified in the .env file

## Setup Instructions

### 1. Configure n8n Workflow

Before running the system, you must:
1. Open your n8n instance
2. Import the workflow file `workflow/ai-chat-agent.json`
3. Ensure the webhook node is active and accessible
4. Note the webhook URL (this will be in the format: `http://localhost:5678/webhook/{id}`)
5. Update the `.env` file in the backend directory with this URL

### 2. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create and configure the .env file:
```bash
cp .env.example .env
```
Update the `.env` file with your n8n webhook URL

4. Start the backend server:
```bash
./run_server.sh
```

The backend will start on `http://localhost:8005`

### 3. Frontend Setup

1. Install required dependencies:
```bash
pip install streamlit requests
```

2. Run the Streamlit application:
```bash
streamlit run frontend/chat_app.py
```

The frontend will be accessible at `http://localhost:8501`

## System Overview

This project consists of two main components:
1. **Backend**: A FastAPI server that acts as a proxy to forward chat messages to an n8n webhook
2. **Frontend**: A Streamlit application that provides a user interface for chatting with the AI agent

## Project Structure

```
.
├── backend/                 # FastAPI backend server
│   ├── main.py              # Main application logic
│   ├── requirements.txt     # Python dependencies
│   ├── run_server.sh        # Server startup script
│   └── README.md            # Backend documentation
├── frontend/                # Streamlit frontend application
│   ├── chat_app.py          # Main Streamlit application
│   └── README.md            # Frontend documentation
├── .gitignore               # Git ignore rules
└── LICENSE                  # MIT License
```

## Backend Setup

### Prerequisites
- Python 3.7+
- pip

### Installation
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file:
```bash
cp .env.example .env
```

4. Update the .env file with your n8n webhook URL

5. Start the server:
```bash
./run_server.sh
```

The backend will start on `http://localhost:8005`

## Frontend Setup

### Prerequisites
- Python 3.7+
- Streamlit
- Requests library

### Installation
1. Install required dependencies:
```bash
pip install streamlit requests
```

2. Run the Streamlit application:
```bash
streamlit run frontend/chat_app.py
```

The frontend will be accessible at `http://localhost:8501`

## API Integration

### Backend API Endpoint
- **Endpoint**: `POST /chat`
- **Request Body**:
```json
{
  "sessionId": "string",
  "chatInput": "string"
}
```
- **Response**: Forwarded response from the n8n webhook

### Frontend Communication
The Streamlit frontend communicates with the backend at `http://localhost:8005/chat` using the same payload format.

## Features

### Backend
- RESTful API with FastAPI
- Asynchronous request forwarding to n8n webhook
- Proper error handling and logging
- Session management
- Timeout handling

### Frontend
- Modern chat interface with message history
- Real-time messaging
- Error handling and loading states
- Session management for conversations
- Responsive design

## Contributing

This project is a demonstration of a chat agent system. For contributions, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.