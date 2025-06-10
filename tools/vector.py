import streamlit as st
from llm import llm, embeddings
from graph import graph

from langchain_neo4j import Neo4jVector
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# Create retriever from your Neo4j basketball match summaries
neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              # (1) Your embedding model
    graph=graph,                             # (2) Your Neo4j graph instance
    index_name="matchSummaries",             # (3) You should create this index on Match nodes
    node_label="Match",                      # (4) Use Match nodes
    text_node_property="summary",            # (5) Summaries as the text content
    embedding_node_property="summary_embedding",  # (6) Embedding as stored string
    retrieval_query="""           
RETURN
    node.summary AS text,
    score,
    {
        match_id: node.id,
        date: node.date,
        team1_score: node.team1_score,
        team2_score: node.team2_score,
        winner: node.winner_team_id
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()

instructions = (
    "You are a helpful assistant answering questions about basketball matches."
    "Use the provided context from past match summaries to respond to the question."
    "If you don't know the answer, say you don't know."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Connect retriever with question-answer logic
match_summary_retriever = create_retrieval_chain(
    retriever,
    question_answer_chain
)

# Function to use in Streamlit or API
def get_match_summary_answer(user_input):
    return match_summary_retriever.invoke({"input": user_input})
