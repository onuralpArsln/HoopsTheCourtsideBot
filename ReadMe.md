# Hoops the Courtside Chatbot 🏀

A Streamlit-based conversational chatbot that leverages a Neo4j graph database and OpenAI LLM to answer questions about movies, actors, and directors.

## Features

- Conversational UI powered by Streamlit
- Integrates with Neo4j for movie knowledge graph queries
- Uses OpenAI's GPT model for natural language understanding
- Session-based chat history stored in Neo4j
- Customizable agent with tool-based reasoning

## Project Structure

```
.
├── agent.py         # Conversational agent logic and orchestration
├── bot.py           # Streamlit UI and main app entry point
├── graph.py         # Neo4j graph connection setup
├── llm.py           # OpenAI LLM configuration
├── utils.py         # Utility functions for Streamlit and session management
├── imgs/            # Images for UI (e.g., bb.png)
├── .streamlit/      # Streamlit configuration and secrets
│   └── secrets.toml
└── .gitignore
```

## Setup

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd HoopsTheCourtsideBot
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

   *(You may need to create `requirements.txt` with packages such as `streamlit`, `langchain`, `langchain-openai`, `langchain-neo4j`, `python-dotenv`.)*

3. **Configure secrets**

   - Edit `.streamlit/secrets.toml` with your Neo4j credentials:

     ```toml
     NEO4J_URI = "bolt://<your-neo4j-host>:7687"
     NEO4J_USERNAME = "<your-username>"
     NEO4J_PASSWORD = "<your-password>"
     ```

   - Set your OpenAI API key in a `.env` file:

     ```
     AI_KEY=sk-...
     ```

4. **Run the app**

   ```sh
   streamlit run bot.py
   ```

## Usage

- Interact with the chatbot via the Streamlit web UI.
- Ask questions about movies, actors, or directors.
- The chatbot will use the Neo4j database to answer your queries.

## File Descriptions

- [`bot.py`](bot.py): Streamlit UI, handles user input and displays chat.
- [`agent.py`](agent.py): Sets up the conversational agent, tools, and memory.
- [`graph.py`](graph.py): Connects to the Neo4j database using Streamlit secrets.
- [`llm.py`](llm.py): Loads OpenAI LLM with API key from environment.
- [`utils.py`](utils.py): Helper functions for message handling and session management.

## Notes

- The chatbot is currently configured for movie-related queries only.
- Make sure your Neo4j instance is running and accessible.

---

*Built with ❤️ using Streamlit, LangChain, Neo4j, and OpenAI.*