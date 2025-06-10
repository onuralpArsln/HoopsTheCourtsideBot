import streamlit as st
from llm import llm
from graph import graph

from langchain_neo4j import GraphCypherQAChain

cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)

def list_all_teams(query=None):
    """
    List all teams in the league with their players
    Args:
        query: The input query (required by LangChain tools but not used in this function)
    """
    query = """
    MATCH (t:Team)
    OPTIONAL MATCH (p:Player)-[:PLAYS_FOR]->(t)
    WITH t, collect(p.name) as players
    RETURN t.name as team_name, players
    ORDER BY t.name
    """
    
    try:
        result = graph.query(query)
        if not result:
            return "No teams found in the database."
        
        response = "Teams in the League:\n\n"
        for team in result:
            response += f"{team['team_name']}:\n"
            if team['players'] and team['players'][0] is not None:
                response += "Players: " + ", ".join(team['players']) + "\n"
            else:
                response += "No players found\n"
            response += "\n"
        
        return response
    except Exception as e:
        return f"An error occurred while fetching team information: {str(e)}"