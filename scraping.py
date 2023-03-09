import requests
import pandas as pd

def get_mlb_teams():
    # get MLB teams
    teams = requests.get('https://statsapi.mlb.com/api/v1/teams', params={'division' : 'Major League Baseball'}).json()
    team_df = {}

    for team in teams['teams']:
        try:
            if team['league']['name'] in ['National League', 'American League']:
                team_df[team['name']] = team['id']
        except KeyError:
            pass

    mlb_teams = pd.DataFrame(team_df, index=[0]).T.reset_index()
    mlb_teams.rename(columns={0: 'team_id', "index" :'team'}, inplace=True)
    return mlb_teams

def get_players_by_league(teams):
    players = {}

    for team in teams['team_id']:
        current_team = requests.get('https://statsapi.mlb.com/api/v1/teams/' + str(team) + '/roster', 
                        params={'rosterType': 'active', 'season' : '2022'}).json()
        for player in current_team['roster']:
            current_player = {}
            current_player['id'] = player['person']['id']
            current_player['position'] = player['position']['abbreviation']
            current_player['status'] = player['status']['code']
            players[player['person']['fullName']] = current_player
    players = pd.DataFrame(players).T.reset_index().rename(columns={'index' : 'player'})
    return players

def create_position_player_stats(playerIDs : list, season : int, startCount = 0, limit = 1000000, minors = False):
    excluded_ids = []
    game_dict = []
    count = 0
    url = "https://statsapi.mlb.com/api/v1/people/"
    for player in playerIDs[startCount:]:
        if minors:
            current_player = requests.get(f"https://statsapi.mlb.com/api/v1/people/{player}/stats?stats=gameLog&gameType=R&leagueListId=milb_all&group=hitting&hydrate=team(league)&language=en&season={season}",).json()
        else:
            current_player = requests.get(url + str(player) + '/stats?season=' + str(season) + '&group=hitting&stats=gameLog',).json()
        # print(current_player)
        try:
            for game in current_player['stats'][0]['splits']:
                game_dict.append({"name": game['player']['fullName'],
                                                    "gameDate": game['date'],
                                                    "gameID": game['game']['gamePk'],
                                                    "team": game['team']['name'],
                                                    "opponent": game['opponent']['name'],
                                                    "league": game['league']['name'],
                                                    "hits": game['stat']['hits'],
                                                    "atBats": game['stat']['atBats'],
                                                    "homeRuns": game['stat']['homeRuns'],
                                                    "runs": game['stat']['runs'],
                                                    "rbi": game['stat']['rbi'],
                                                    "stolenBases": game['stat']['stolenBases'],
                                                    "strikeOuts": game['stat']['strikeOuts'],
                                                    "walks": game['stat']['baseOnBalls'],
                                                    "avg": game['stat']['avg'],
                                                    "obp": game['stat']['obp'],
                                                    "slg": game['stat']['slg'],
                                                    "ops": game['stat']['ops'],})
            count += 1
        except IndexError or gaierror:
            excluded_ids.append(player)
        # except KeyError:
        #     pass
        
        # if count % 1000 == 0:
        #     print(count)
        if count == limit:
            break
    return pd.DataFrame(game_dict), excluded_ids

def create_pitcher_stats(playerIDs : list, season : int, startCount = 0, limit = 1000000, minors = False):
    excluded_ids = []
    game_dict = []
    count = 0
    url = "https://statsapi.mlb.com/api/v1/people/"
    for player in playerIDs[startCount:]:
        if minors:
            current_player = requests.get(f"https://statsapi.mlb.com/api/v1/people/{player}/stats?stats=gameLog&gameType=R&leagueListId=milb_all&group=pitching&hydrate=team(league)&language=en&season={season}",).json()
        else:
            current_player = requests.get(url + str(player) + '/stats?season=' + str(season) + '&group=hitting&stats=gameLog',).json()
        # print(current_player)
        try:
            for game in current_player['stats'][0]['splits']:
                game_dict.append({"name": game['player']['fullName'],
                                                    "gameDate": game['date'],
                                                    "gameID": game['game']['gamePk'],
                                                    "team": game['team']['name'],
                                                    "opponent": game['opponent']['name'],
                                                    "league": game['league']['name'],
                                                    "hits": game['stat']['hits'],
                                                    "battersFaced": game['stat']['battersFaced'],
                                                    "homeRuns": game['stat']['homeRuns'],
                                                    "runs": game['stat']['runs'],
                                                    "earnedRuns": game['stat']['earnedRuns'],
                                                    "strikeOuts": game['stat']['strikeOuts'],
                                                    "walks": game['stat']['baseOnBalls'],
                                                    "inningPitched": game['stat']['inningsPitched'],
                                                    "era": game['stat']['era'],
                                                    "totalBases": game['stat']['totalBases'],
                                                    "whip": game['stat']['whip'],
                                                    "gamesStarted": game['stat']['gamesStarted'],
                                                    "wins": game['stat']['wins'],
                                                    "losses": game['stat']['losses'],
                                                    "saves": game['stat']['saves'],
                                                    "blownSaves": game['stat']['blownSaves'],
                                                    "outs": game['stat']['outs'],
                                                    "strikes": game['stat']['strikes'],
                                                    "numberOfPitches": game['stat']['numberOfPitches'],})
            count += 1
        except IndexError or gaierror:
            excluded_ids.append(player)
        except KeyError:
            pass
        
        # if count % 1000 == 0:
        #     print(count)
        if count == limit:
            break
    return pd.DataFrame(game_dict), excluded_ids