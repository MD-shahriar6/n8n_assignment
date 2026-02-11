# AI Chat Agent - Frontend

This is the frontend application for the AI chat agent system built with Streamlit.

## Features

- Modern chat interface with message history
- Real-time messaging with AI agent
- Error handling and loading states
- Session management for conversations
- Responsive design

## Prerequisites

- Python 3.7+
- Streamlit
- Requests library

## Installation

1. Install required dependencies:
```bash
pip install streamlit requests
```

2. Make sure the backend server is running (see backend README for instructions)

3. The frontend will automatically read the webhook URL from the .env file in the backend directory

## Usage

Run the Streamlit application:
```bash
streamlit run frontend/chat_app.py
```

The application will be accessible at http://localhost:8501

## File Structure

```
frontend/
├── chat_app.py          # Main Streamlit application
└── README.md            # This documentation
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8005/chat` with the following payload format:
```json
{
  "sessionId": "string",
  "chatInput": "string"
}
```

## Contributing

This project is a simple demonstration. For contributions, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.