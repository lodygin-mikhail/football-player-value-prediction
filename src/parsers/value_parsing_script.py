#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np


def get_players_value(link):

    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page_club = 'https://www.transfermarkt.com' + link
    tree = requests.get(page_club, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    player_data = {
        'player': [],
        'value': []
    }

    for x in soup.find_all('td', {'class': 'hauptlink'})[:-7:2]:
        player_data['player'].append(x.text.strip())
    
    for x in soup.find_all('td', {'class': 'hauptlink'})[1:-7:2]:
        value = x.text.strip()[1:-1]
        if '.' not in value:
            try:
                player_data['value'].append(float('0.' + value[0]))
            except:
                player_data['value'].append(np.nan)
        else:
            player_data['value'].append(float(value))

    return pd.DataFrame(player_data)


def get_league_players_value(link):

    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page_league = 'https://www.transfermarkt.com' + link
    tree = requests.get(page_league, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    teams_links = {}

    for x in soup.find_all('td', {'class': 'hauptlink no-border-links'}):
        teams_links[x.text] = x.a['href']
        
    list_of_team_dfs = []

    for team in teams_links:
        list_of_team_dfs.append(get_players_value(teams_links[team]))
        time.sleep(2)

    return pd.concat(list_of_team_dfs)


def get_leagues_values():

    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page_league = 'https://www.transfermarkt.com/wettbewerbe/europa'
    tree = requests.get(page_league, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    league_links = {}
    
    for x in soup.find_all('a', {'class':'tm-button-list__list-item tm-button-list__list-item--big'})[:-1]:
        league_links[x['title']] = x['href']
        
    list_of_league_dfs = []

    for league in league_links:
        list_of_league_dfs.append(get_league_players_value(league_links[league]))
        time.sleep(2)

    return pd.concat(list_of_league_dfs)
