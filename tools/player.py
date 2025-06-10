from graph import graph

def get_player_info(player_name: str) -> str:
    """
    Get comprehensive information about a player including:
    - Teams they played for
    - Number of matches played
    - Teammates
    - Scoring statistics
    - Performance against different teams
    """
    query = """
    MATCH (p:Player {name: $player_name})
    OPTIONAL MATCH (p)-[:PLAYED_FOR]->(t:Team)
    OPTIONAL MATCH (p)-[:PLAYED_IN]->(m:Match)
    OPTIONAL MATCH (m)-[:HOME_TEAM|AWAY_TEAM]->(opp:Team)
    OPTIONAL MATCH (p)-[:SCORED]->(s:Score)
    WITH p, 
         collect(DISTINCT t.name) as teams,
         count(DISTINCT m) as matches_played,
         collect(DISTINCT opp.name) as opponents,
         sum(s.points) as total_points
    RETURN {
        name: p.name,
        teams: teams,
        matches_played: matches_played,
        opponents: opponents,
        total_points: total_points
    } as player_info
    """
    
    result = graph.query(query, {"player_name": player_name})
    
    if not result:
        return f"No information found for player {player_name}"
    
    player_data = result[0]["player_info"]
    
    # Format the response
    response = f"Player Information for {player_data['name']}:\n"
    response += f"Teams played for: {', '.join(player_data['teams'])}\n"
    response += f"Total matches played: {player_data['matches_played']}\n"
    response += f"Total points scored: {player_data['total_points']}\n"
    response += f"Opponents faced: {', '.join(player_data['opponents'])}\n"
    
    return response

def get_player_teammates(player_name: str) -> str:
    """
    Get information about a player's teammates throughout their career
    """
    query = """
    MATCH (p:Player {name: $player_name})-[:PLAYED_FOR]->(t:Team)
    MATCH (teammate:Player)-[:PLAYED_FOR]->(t)
    WHERE teammate.name <> p.name
    WITH t, collect(DISTINCT teammate.name) as teammates
    RETURN t.name as team, teammates
    """
    
    result = graph.query(query, {"player_name": player_name})
    
    if not result:
        return f"No teammate information found for player {player_name}"
    
    response = f"Teammates of {player_name}:\n"
    for record in result:
        response += f"\nTeam: {record['team']}\n"
        response += f"Teammates: {', '.join(record['teammates'])}\n"
    
    return response

def get_player_scoring_stats(player_name: str) -> str:
    """
    Get detailed scoring statistics for a player
    """
    query = """
    MATCH (p:Player {name: $player_name})-[s:SCORED]->(m:Match)
    MATCH (m)-[:PLAYED]-(opp:Team)
    WHERE opp <> (p)-[:PLAYS_FOR]->()
    WITH p, opp, sum(s.points) as points_against
    ORDER BY points_against DESC
    RETURN opp.name as opponent, points_against
    """
    
    result = graph.query(query, {"player_name": player_name})
    
    if not result:
        return f"No scoring statistics found for player {player_name}"
    
    response = f"Scoring Statistics for {player_name}:\n"
    for record in result:
        response += f"\nAgainst {record['opponent']}: {record['points_against']} points"
    
    return response 