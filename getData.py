from bs4 import BeautifulSoup
import requests
import random
from math import ceil

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    }

def get_games():
    url = "https://futebolcapixaba.com/campeonatos/estadual-sub-20-2025/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        table = tables[1] if len(tables) > 1 else None 
        if table:
            rows = table.find_all("tr")
            games = []
            for row in rows[1:]:
                cols = row.find_all("td")
                games.append([col.text.strip() for col in cols])
            return games
        else:
            print("No table found on the page.")
            return []
    else:
        print("Failed to retrieve games from the website.")
        return []

def get_game_links():
    url = "https://futebolcapixaba.com/campeonatos/estadual-sub-20-2025/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        table = tables[1] if len(tables) > 1 else None
        if table:
            rows = table.find_all("tr")
            links = []
            for row in rows[1:]:
                link_cell = row.find("td", class_="data-time ok")
                if link_cell and link_cell.find("a"):
                    links.append(link_cell.find("a")["href"])
            return links
        else:
            print("No table found on the page.")
            return []
    else:
        print("Failed to retrieve links from the website.")
        return []
    
def match_data(link_match):
    site = requests.get(link_match, headers={'User-Agent': random.choice(user_agents_list)},verify=False)
    soup = BeautifulSoup(site.content, 'html.parser')
    location = soup.find(class_='styles_localData__rN9lF')
    spans = location.find_all("span") if location else []
    location_data = [span.text.strip() for span in spans]
    return(location_data)

def get_teams(link_match):
    site = requests.get(link_match, headers={'User-Agent': random.choice(user_agents_list)},verify=False)
    soup = BeautifulSoup(site.content, 'html.parser')
    teams = []
    team_elements = soup.find_all("a", class_='styles_clubContainer__5olkH')
    for team_element in team_elements:
        team_name = team_element.find("strong").text.strip() if team_element.find("strong") else None
        if team_name:
            teams.append(team_name)
    return(teams)
