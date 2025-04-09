import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Campeonatos Temporada 2025", layout="wide")
st.title("Campeonato Estadual Sub-20")

today = datetime.today()

links_serieD = [
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-nova-iguacu/830096",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-boavista-saf/830131",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-porto-vitoria-f-c/830345",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-agua-santa/830389",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-portuguesa/830420",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-nova-iguacu/830453",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-boavista-saf/830483",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-pouso-alegre/830517",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-marica/830550",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-agua-santa/830583",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-portuguesa/830620",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-rio-branco-a-c-saf/830653",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/porto-vitoria-f-c-x-pouso-alegre/830683",
    "https://cbf.com.br/futebol-brasileiro/jogos/campeonato-brasileiro/serie-d/2025/rio-branco-a-c-saf-x-marica/830717"
]





def get_games():
    url = "https://futebolcapixaba.com/campeonatos/capixabao-2025/"
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
    df["Data_DT"] = pd.to_datetime(df["Data"])
    df["Dia da Semana"] = df["Data_DT"].dt.day_name(locale="pt_BR")
    df["Placar"] = df["Placar"].apply(lambda x: x if len(x.strip()) <= 6 else " - ")
    df_next = df[df["Data"] >= today.strftime("%Y-%m-%d")]
    df_next = df_next.sort_values(by="Data")
    df_next = df_next[["Rodada", "Data", "Hora", "Dia da Semana", "Mandante", "Visitante", "Estádio", "Link"]]
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
    df_last = df_last[["Rodada", "Data", "Mandante", "Placar", "Visitante", "Estádio", "Link"]]
    st.data_editor(
        df_last,
        column_config={
        "Link": st.column_config.LinkColumn("Link")
    },
    hide_index=True
)
else:
    st.write("Nenhum jogo encontrado.")