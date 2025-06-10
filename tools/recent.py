from graph import graph
from llm import llm
from langchain_core.prompts import ChatPromptTemplate
from tools.team import get_team_info
from tools.vector import get_match_summary_answer


def get_recent_match_info(query):
    """
    Get information about a team's most recent match by combining team and match data
    """
    # First get team info to identify the team
    team_info = get_team_info(query)
    
    # Extract team name from the response
    if "Team:" in team_info:
        team_name = team_info.split("Team:")[1].split("\n")[0].strip()
        
        # Query Neo4j for the most recent match
        recent_match_query = """
        MATCH (t:Team)
        WHERE t.name = $team_name
        MATCH (t)-[:PLAYED]->(m:Match)
        WITH t, m
        ORDER BY m.date DESC
        LIMIT 1
        MATCH (opp:Team)-[:PLAYED]->(m)
        WHERE opp <> t
        RETURN {
            match_id: m.id,
            date: m.date,
            opponent: opp.name,
            team_score: CASE WHEN (t)-[:WON]->(m) THEN m.team1_score ELSE m.team2_score END,
            opponent_score: CASE WHEN (t)-[:WON]->(m) THEN m.team2_score ELSE m.team1_score END,
            result: CASE WHEN (t)-[:WON]->(m) THEN 'Won' ELSE 'Lost' END,
            summary: m.summary
        } as match_info
        """
        
        try:
            result = graph.query(recent_match_query, {"team_name": team_name})
            if result:
                match_info = result[0]["match_info"]
                
                response = f"""
                Most Recent Match for {team_name}:
                Date: {match_info['date']}
                Opponent: {match_info['opponent']}
                Score: {match_info['team_score']} - {match_info['opponent_score']}
                Result: {match_info['result']}
                """
                
                # Add match summary if available
                if match_info.get('summary'):
                    response += f"\nMatch Summary:\n{match_info['summary']}"
                
                return response
            else:
                return f"I couldn't find any recent matches for {team_name}."
        except Exception as e:
            return f"An error occurred while searching for recent match information: {str(e)}"
    else:
        return team_info

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a basketball enthusiast providing information about NBA and basketball."),
    ("human", "{input}"),
])