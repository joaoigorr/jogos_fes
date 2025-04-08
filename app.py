import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Campeonatos Temporada 2025", layout="wide")
st.title("Campeonato Estadual Sub-20")

today = datetime.today()

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
            st.error("No table found on the page.")
            return []
    else:
        st.error("Failed to retrieve games from the website.")
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
            st.error("No table found on the page.")
            return []
    else:
        st.error("Failed to retrieve links from the website.")
        return []

games = get_games()
links = get_game_links()
if games:
    df_games = pd.DataFrame(games)
    df_links = pd.DataFrame(links)
    df = pd.concat([df_games, df_links], axis=1)
    df.columns = ["Data", "Mandante", "Placar", "Visitante", "Estádio", "Rodada","Link"]
    df["Hora"] = df["Data"].str[11:16]
    df["Data"] = df["Data"].str[:10]
    df["Dia da Semana"] = pd.to_datetime(df["Data"]).dt.day_name(locale='pt_BR')
    df["Placar"] = df["Placar"].apply(lambda x: x if len(x.strip()) <= 6 else " - ")
    df_next = df[df["Data"] >= today.strftime("%Y-%m-%d")]
    df_next = df_next.sort_values(by="Data")
    df_next = df_next[["Rodada", "Data", "Hora","Dia da Semana", "Mandante", "Placar", "Visitante", "Estádio", "Link"]]
    st.write("Próximos Jogos:")
    st.data_editor(
        df_next,
        column_config={
        "Link": st.column_config.LinkColumn("Link")
    },
    hide_index=True
)
    st.write("Últimos Jogos:")
    df_last = df[df["Data"] < today.strftime("%Y-%m-%d")]
    df_last = df_last.sort_values(by="Data", ascending=False)
    df_last = df_last[["Rodada", "Data", "Hora","Dia da Semana", "Mandante", "Placar", "Visitante", "Estádio", "Link"]]
    st.data_editor(
        df_last,
        column_config={
        "Link": st.column_config.LinkColumn("Link")
    },
    hide_index=True
)
else:
    st.write("Nenhum jogo encontrado.")