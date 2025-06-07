import streamlit as st
from utils import write_message
from agent import generate_response
from pathlib import Path


# Page Config
st.set_page_config(
    page_title="Hoops the Courtside Chatbot",
    page_icon="🏀",
    initial_sidebar_state="expanded",
)



st.markdown(
    """
    <style>
    .bouncing-ball {
        font-size: 60px;
        display: inline-block;
        position: relative;
    }
    .bouncing-ball:hover {
        font-size: 60px;
        display: inline-block;
        animation: bounce 1s infinite;
        position: relative;
    }

    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-30px);
        }
    }
    </style>

    <div style="text-align: center; padding: 20px;">
        <div class="bouncing-ball">🏀</div>
    </div>

 

    """,
    unsafe_allow_html=True
)




# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm Hoops the Courtside Chatbot,  How can I help you?"},
    ]

# Submit handler
def handle_submit(message):
    """
    Submit handler:

    You will modify this method to talk with an LLM and provide
    context using data from Neo4j.
    """

    # Handle the response
    with st.spinner('Throwing awesome three pointers...'):
        # Call the agent
        response = generate_response(message)
        write_message('assistant', response)
        


# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    write_message('user', prompt)

    # Generate a response
    handle_submit(prompt)


# streamlit run bot.py