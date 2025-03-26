#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_players_data(link,num_of_players=24):
        
    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page_clubs1 = 'https://fbref.com' + link
    tree = requests.get(page_clubs1, headers=headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    
    #инициализируем словарь, в который будем добавлять ссылки на страницы команд
    team_urls = {}

    team_names = soup.find_all('td', {'class': 'left', 'data-stat': 'team'})
    for x in team_names[:len(team_names) // 2]:
        team_urls[x.text[1:]] = x.a['href']

    all_players_data = {
    }

    #инициализируем два словаря со списками в ключах, куда будем добавлять данные
    player_data = {
            'player': [],
            'club': [],
            'nationality': [],
            'age': [],
            'position': []
    }

    metrics_data = {
    }
    
    table_of_metrics = {'stats_standard_9': [],
                        'stats_shooting_9': [],
                        'stats_passing_9': [],
                        'stats_passing_types_9': [],
                        'stats_gca_9': [],
                        'stats_defense_9': [],
                        'stats_possession_9': [],
                        'stats_playing_time_9': [],
                        'stats_misc_9': []
    }

    
    page_club2 = 'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats'
    tree1 = requests.get(page_club2, headers = headers)
    soup1 = BeautifulSoup(tree1.content, 'html.parser')
    
    # заполним словарь различными метриками
    for x in soup1.find_all('table', {'id': 'stats_standard_9'})[0]('td', {'class': 'right'})[:29]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_standard_9'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': 'stats_shooting_9'})[0].find_all('td', {'class': 'right'})[2:18]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_shooting_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_passing_9'})[0].find_all('td', {'class': 'right'})[1:24]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_passing_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_passing_types_9'})[0].find_all('td', {'class': 'right'})[1:16]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_passing_types_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_gca_9'})[0].find_all('td', {'class': 'right'})[1:17]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_gca_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_defense_9'})[0].find_all('td', {'class': 'right'})[1:17]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_defense_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_possession_9'})[0].find_all('td', {'class': 'right'})[1:23]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_possession_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_playing_time_9'})[0].find_all('td', {'class': 'right'})[4:22]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_playing_time_9'].append(x['data-stat'])
    
    for x in soup1.find_all('table', {'id': 'stats_misc_9'})[0].find_all('td', {'class': 'right'})[1:17]:
        metrics_data[x['data-stat']] = []
        table_of_metrics['stats_misc_9'].append(x['data-stat'])


    for curr_team in team_urls:
        
        page_club3 = 'https://fbref.com' + team_urls[curr_team]
        tree2 = requests.get(page_club3, headers = headers)
        soup2 = BeautifulSoup(tree2.content, 'html.parser')
        
        # заполним списки осн. информации о игроке в словаре
        for x in soup2.find_all('th', {'class': 'left', 'scope': 'row', 'data-stat': 'player'})[:num_of_players]:
           player_data['player'].append(x.text)

        for i in range(num_of_players):
            player_data['club'].append(curr_team)
    
        for x in soup2.find_all('td', {'class': 'left poptip', 'data-stat': 'row', 'data-stat': 'nationality'})[:num_of_players]:
            player_data['nationality'].append(x.text)
    
        for x in ['age', 'position']:
            for y in soup2.find_all('td', {'class': 'center', 'data-stat': x})[:num_of_players]:
                player_data[x].append(y.text)
            
        # заполним списки метрик игрока в словаре
        used_metrics = []
    
        for x in ['stats_standard_9', 'stats_shooting_9', 'stats_passing_9', 'stats_passing_types_9', 'stats_gca_9', 'stats_defense_9', 'stats_possession_9', 'stats_playing_time_9', 'stats_misc_9']:
            for y in metrics_data:
                if (y in table_of_metrics[x]) and (y not in used_metrics):
                    for z in soup1.find_all('table', {'id': x})[0].find_all('td', {'class': 'right', 'data-stat': y})[:num_of_players]:
                        metrics_data[y].append(z.text)
                        used_metrics.append(y)
        time.sleep(2)
    
    all_players_data = player_data | metrics_data
    return pd.DataFrame(all_players_data)



def get_team_data(league, team, num_of_players):
    
    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page_club = 'https://fbref.com' + team_urls[team]
    tree1 = requests.get(page_club, headers = headers)
    soup1 = BeautifulSoup(tree1.content, 'html.parser')

    #инициализируем два словаря со списками в ключах, куда будем добавлять данные
    player_data = {
        'player': [],
        'club': [],
        'league': [],
        'nationality': [],
        'age': [],
        'position': []
    }

    metrics_data = {
                    }

    league_num = {
        'Premier League': 9,
        'Serie A': 11,
        'Ligue 1': 13,
        'La Liga': 12,
        'Bundesliga': 20
    }
    
    table_of_metrics = {
        f'stats_standard_{league_num[league]}': [],
        f'stats_shooting_{league_num[league]}': [],
        f'stats_passing_{league_num[league]}': [],
        f'stats_passing_types_{league_num[league]}': [],
        f'stats_gca_{league_num[league]}': [],
        f'stats_defense_{league_num[league]}': [],
        f'stats_possession_{league_num[league]}': [],
        f'stats_playing_time_{league_num[league]}': [],
        f'stats_misc_{league_num[league]}': []
    }
    
    # дополним словарь различными метриками
    for x in soup1.find_all('table', {'id': f'stats_standard_{league_num[league]}'})[0]('td', {'class': 'right'})[:29]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_standard_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_shooting_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:18]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_shooting_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_passing_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:24]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_passing_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_passing_types_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:16]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_passing_types_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_gca_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:17]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_gca_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_defense_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:17]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_defense_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_possession_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:23]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_possession_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_playing_time_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:22]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_playing_time_{league_num[league]}'].append(x['data-stat'])

    for x in soup1.find_all('table', {'id': f'stats_misc_{league_num[league]}'})[0].find_all('td', {'class': 'right'})[:17]:
        metrics_data[x['data-stat']] = []
        table_of_metrics[f'stats_misc_{league_num[league]}'].append(x['data-stat'])

    # заполним списки осн. информации о игроке в словаре
    for x in soup1.find_all('th', {'class': 'left', 'scope': 'row', 'data-stat': 'player'})[:num_of_players]:
        player_data['player'].append(x.text)

    for i in range(num_of_players):
        player_data['club'].append(team)

    for i in range(num_of_players):
        player_data['league'].append(league)

    for x in soup1.find_all('td', {'class': 'left poptip', 'data-stat': 'row', 'data-stat': 'nationality'})[:num_of_players]:
        player_data['nationality'].append(x.text)

    for x in ['age', 'position']:
        for y in soup1.find_all('td', {'class': 'center', 'data-stat': x})[:num_of_players]:
            player_data[x].append(y.text)
        
    # заполним списки метрик игрока в словаре
    used_metrics = []
    
    for x in [f'stats_standard_{league_num[league]}', f'stats_shooting_{league_num[league]}', f'stats_passing_{league_num[league]}', 
              f'stats_passing_types_{league_num[league]}', f'stats_gca_{league_num[league]}', f'stats_defense_{league_num[league]}', 
              f'stats_possession_{league_num[league]}', f'stats_playing_time_{league_num[league]}', f'stats_misc_{league_num[league]}']:
        for y in metrics_data:
            if (y in table_of_metrics[x]) and (y not in used_metrics):
                for z in soup1.find_all('table', {'id': x})[0].find_all('td', {'class': 'right', 'data-stat': y})[:num_of_players]:
                    metrics_data[y].append(z.text)
                    used_metrics.append(y)

    data = player_data | metrics_data

    return pd.DataFrame(data)


def get_league_players_data(league):
    global team_urls

    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    league_page = {
        'Premier League': 'https://fbref.com/en/comps/9/Premier-League-Stats',
        'Serie A': 'https://fbref.com/en/comps/11/Serie-A-Stats',
        'Ligue 1': 'https://fbref.com/en/comps/13/Ligue-1-Stats',
        'La Liga': 'https://fbref.com/en/comps/12/La-Liga-Stats',
        'Bundesliga': 'https://fbref.com/en/comps/20/Bundesliga-Stats'
    }

    page_clubs1 = league_page[league]
    tree = requests.get(page_clubs1, headers=headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    #инициализируем словарь, в который будем добавлять ссылки на страницы команд
    team_urls = {}

    team_names = soup.find_all('td', {'class': 'left', 'data-stat': 'team'})
    for x in team_names[:len(team_names) // 2]:
        team_urls[x.text[1:]] = x.a['href']

    list_of_teams = list(team_urls.keys())

    list_of_team_data = []

    for team in list_of_teams:
        list_of_team_data.append(get_team_data(league, team, num_of_players=24))
        time.sleep(1)
        
    return pd.concat(list_of_team_data)

def get_all_leagues_data():
    league_dfs = []
    
    for league in ['Premier League', 'Serie A', 'Ligue 1', 'La Liga', 'Bundesliga']:
        league_dfs.append(get_league_players_data(league))
        print(f'Done: {league}')
        time.sleep(1)
        
    return pd.concat(league_dfs)




