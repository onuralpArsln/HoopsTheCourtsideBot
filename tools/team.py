from graph import graph
from llm import llm
from langchain_core.prompts import ChatPromptTemplate

def get_team_info(query):
    """
    Query Neo4j for team information based on the user's question.
    """
    # First, use LLM to extract team name from the query
    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the team name from the following question. Return only the team name, nothing else. If you can't identify a specific team, return 'unknown'."),
        ("human", "{query}")
    ])
    
    # Get the response and extract the content
    response = llm.invoke(extract_prompt.format(query=query))
    team_name = response.content if hasattr(response, 'content') else str(response)
    
    if team_name.lower() == 'unknown':
        return "I couldn't identify a specific team from your question. Please try asking about a specific team."
    
    # Query Neo4j for team information
    team_query = """
    MATCH (t:Team)
    WHERE t.name CONTAINS $team_name
    OPTIONAL MATCH (p:Player)-[:PLAYS_FOR]->(t)
    OPTIONAL MATCH (t)-[r:PLAYED]->(m:Match)
    WITH t, 
         collect(DISTINCT p.name) as players,
         count(DISTINCT m) as total_matches,
         count(DISTINCT CASE WHEN t.id = m.winner_team_id THEN m END) as wins
    RETURN {
        team_name: t.name,
        players: players,
        total_matches: total_matches,
        wins: wins,
        win_percentage: CASE WHEN total_matches > 0 THEN toFloat(wins)/total_matches * 100 ELSE 0 END
    } as team_info
    """
    
    try:
        result = graph.query(team_query, {"team_name": team_name})
        
        if not result:
            return f"I couldn't find any information about the team '{team_name}'."
        
        team_info = result[0]["team_info"]
        
        # Format the response
        response = f"""
        Team: {team_info['team_name']}
        Total Matches: {team_info['total_matches']}
        Wins: {team_info['wins']}
        Win Percentage: {team_info['win_percentage']:.1f}%
        
        Players:
        {', '.join(team_info['players']) if team_info['players'] else 'No players found'}
        """
        
        return response
    except Exception as e:
        return f"An error occurred while searching for team information: {str(e)}" 