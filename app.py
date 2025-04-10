import streamlit as st
import pandas as pd
from datetime import datetime
import time
from getData import *

st.set_page_config(page_title="Campeonatos Temporada 2025", layout="wide")
st.title("Próximos Jogos Para Scouts - ES")
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


with st.spinner("Carregando Copa ES..."):
    games = get_games()
    links = get_game_links()
    st.write("COPA ES - 2025")
    df_games = pd.DataFrame(games)
    df_links = pd.DataFrame(links)
    df = pd.concat([df_games, df_links], axis=1)
    df.columns = ["Data", "Mandante", "Placar", "Visitante", "Estádio", "Rodada","Link"]
    df["Hora"] = df["Data"].str[11:16]
    df["Data"] = df["Data"].str[:10]
    df["Data_DT"] = pd.to_datetime(df["Data"])
    df["Dia da Semana"] = df["Data_DT"].dt.day_name()
    df["Placar"] = df["Placar"].apply(lambda x: x if len(x.strip()) <= 6 else " - ")
    df_next = df[df["Data"] >= today.strftime("%Y-%m-%d")]
    df_next = df_next.sort_values(by="Data")
    df_next = df_next[["Rodada", "Data", "Hora", "Dia da Semana", "Mandante", "Visitante", "Estádio", "Link"]]
    st.data_editor(
        df_next,
        column_config={
        "Link": st.column_config.LinkColumn("Link")
    },
    hide_index=True
    )

serie_d = []

with st.spinner("Carregando Serie D..."):
    for link in links_serieD:
        data = match_data(link)
        teams = get_teams(link)
        mandante = teams[0]
        visitante = teams[1]
        hora = data[0]
        dia = data[1]
        estadio = data[2]
        serie_d.append([dia, hora, mandante, visitante, estadio, link])

    df_serie_d = pd.DataFrame(serie_d, columns=["Data","Hora","Mandante", "Visitante", "Estádio", "Link"])
    st.write("Campeonato Brasileiro Série D")
    st.data_editor(
        df_serie_d,
        column_config={
            "Link": st.column_config.LinkColumn("Link")
        },
        hide_index=True
    )