from llm import llm
from graph import graph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_neo4j import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from utils import get_session_id
from tools.vector import get_match_summary_answer
from tools.team import get_team_info
from tools.cypher import cypher_qa, list_all_teams
from tools.recent import get_recent_match_info, chat_prompt
from tools.player import get_player_info, get_player_teammates, get_player_scoring_stats



basketball_chat = chat_prompt | llm | StrOutputParser()

tools = [
    Tool.from_function(
        name="List All Teams",
        description="Use this tool to get a list of all teams in the league and their players.",
        func=list_all_teams,
    ),
    Tool.from_function(
        name="Recent Match Information",
        description="Use this tool for questions about a team's most recent match, including the score, opponent, and match summary.",
        func=get_recent_match_info,
    ),
    Tool.from_function(
        name="Team Information",
        description="Use this tool for general team information including overall performance, players, and match history.",
        func=get_team_info,
    ),
    Tool.from_function(
        name="Match Summary Search",
        description="ONLY use this tool for finding specific details about what happened during a particular match (e.g., specific plays, events, or moments in a game).",
        func=get_match_summary_answer,
    ),
    Tool.from_function(
        name="League Information",
        description="Use this tool for league-wide queries about schedules, standings, or general league statistics.",
        func=cypher_qa,
    ),
    Tool.from_function(
        name="Player Information",
        description="Use this tool for comprehensive player information including teams played for, matches played, teammates, and scoring statistics.",
        func=get_player_info,
    ),
    Tool.from_function(
        name="Player Teammates",
        description="Use this tool to find out who a player's teammates were throughout their career.",
        func=get_player_teammates,
    ),
    Tool.from_function(
        name="Player Scoring Statistics",
        description="Use this tool to get detailed scoring statistics for a player, including points scored against different teams.",
        func=get_player_scoring_stats,
    ),
    Tool.from_function(
        name="General Chat",
        description="Use this tool only for general basketball chat not covered by other tools.",
        func=basketball_chat.invoke,
    ),
]

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

agent_prompt = PromptTemplate.from_template("""
You are a basketball enthusiast providing information about basketball matches.
Be as helpful as possible and return as much information as possible.
Do not answer any questions that do not relate to basketball, when asked about a name ensure if they are a basketball team or player.

Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.

TOOLS:
------

You have access to the following tools:

{tools}

IMPORTANT TOOL SELECTION RULES:
1. For questions about a team's most recent match (e.g., "how was last match", "what happened in their last game"), ALWAYS use the "Recent Match Information" tool FIRST.
2. For general team information (performance, players, overall history), use the "Team Information" tool.
3. For specific match details (plays, events, moments), use the "Match Summary Search" tool.
4. For league-wide queries (schedules, standings), use the "League Information" tool.
5. For player-related questions (teams played for, matches played, teammates, scoring stats), use the "Player Information", "Player Teammates", or "Player Scoring Statistics" tools.
6. Use "General Chat" only as a last resort.

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

chat_agent = RunnableWithMessageHistory(
    agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def generate_response(user_input):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """
    response = chat_agent.invoke(
        {"input": user_input},
        {"configurable": {"session_id": get_session_id()}},
    )
    return response['output']