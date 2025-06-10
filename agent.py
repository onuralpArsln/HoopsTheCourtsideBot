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

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a basketball enthusiast providing information about NBA and basketball."),
        ("human", "{input}"),
    ]
)

basketball_chat = chat_prompt | llm | StrOutputParser()

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general basketball chat not covered by other tools",
        func=basketball_chat.invoke,
    ),
    Tool.from_function(
        name="Match Summary Search",  
        description="For when you need to find information about matches, teams and players about events, results or performance",
        func=get_match_summary_answer, 
    ),
    Tool.from_function(
        name="Team Information",
        description="For when you need to find specific information about teams, their players, and team statistics",
        func=get_team_info,
    )
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
    verbose=True
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
        {"configurable": {"session_id": get_session_id()}},)

    return response['output']