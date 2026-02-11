import streamlit as st
import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the page configuration
st.set_page_config(
    page_title="MeetSync",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 4px solid #9e9e9e;
    }
    .message-time {
        font-size: 0.7em;
        color: #666;
        margin-top: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(int(time.time()))

# Title
st.title("🤖 MeetSync: Schedule a meeting with me.")
st.markdown("Welcome! Start chatting with the AI agent below.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.markdown(f"<div class='message-time'>{message['timestamp']}</div>", unsafe_allow_html=True)

# Get user input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
        st.markdown(f"<div class='message-time'>{datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
    
    # Send message to backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Prepare payload
        payload = {
            "sessionId": st.session_state.session_id,
            "chatInput": user_input
        }
        
        # Get backend URL from environment
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8005/chat")
        
        try:
            with st.spinner("AI is thinking..."):
                response = requests.post(
                    backend_url,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=300
                )
                
            if response.status_code == 200:
                # Parse the response
                result = response.json()
                bot_response = result.get("output", "No output received")
                
                # Display the response
                full_response = bot_response
                message_placeholder.markdown(full_response)
                
                # Add bot response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                message_placeholder.markdown(f"❌ **Error**: {error_msg}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {response.status_code}",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            message_placeholder.markdown(f"❌ **Error**: {error_msg}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Connection error: {str(e)}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            message_placeholder.markdown(f"❌ **Error**: {error_msg}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Unexpected error: {str(e)}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })