
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

def tratar_dados_faltantes(df):
    df["Cliques no link únicos"].fillna(0, inplace=True)
    df["Custo por clique no link único"].fillna(0, inplace=True)
    df["CTR único (taxa de cliques no link)"].fillna(0, inplace=True)
    df["Custo por resultado"].fillna(0, inplace=True)
    df["Engajamento com a Página"].fillna(0, inplace=True)
    df["Engajamentos com a publicação"].fillna(0, inplace=True)
    df["Reações à publicação"].fillna(0, inplace=True)
    df["Salvamentos da publicação"].fillna(0, inplace=True)
    df["Compartilhamentos da publicação"].fillna(0, inplace=True)
    df["Custo por engajamento com a Página"].fillna(0, inplace=True)
    df["Custo por engajamento com a publicação"].fillna(0, inplace=True)
    
    df["call_to_action_type"].fillna("não utilizado", inplace=True)
    df["Tipo de resultado"].fillna("não utilizado", inplace=True)
    df["Públicos personalizados excluídos"].fillna("não utilizado", inplace=True)
    df["Públicos personalizados incluídos"].fillna("não utilizado", inplace=True)

    
def tratar_tipos_dados(df):
    df["Dia"] = pd.to_datetime(df["Dia"])
    df["Início"] = pd.to_datetime(df["Início"])
    df["Início dos relatórios"] = pd.to_datetime(df["Início dos relatórios"])
    # df["Término"].value_counts()
    # df["Término"] = pd.to_datetime(df["Término"])
    df["Término dos relatórios"] = pd.to_datetime(df["Término dos relatórios"])

    df["Nome da campanha"] = df["Nome da campanha"].astype(str)
    df["Nome do conjunto de anúncios"] = df["Nome do conjunto de anúncios"].astype(str)
    df["Nome do anúncio"] = df["Nome do anúncio"].astype(str)

    df["Orçamento da campanha"] = df["Orçamento da campanha"].astype(float)

    df["Valor usado (BRL)"] = df["Valor usado (BRL)"].astype(float)


    df["Alcance"] = df["Alcance"].astype(int)
    df["Frequência"] = df["Frequência"].astype(int)
    df["Impressões"] = df["Impressões"].astype(int)

    df["Resultados"].fillna(0,inplace=True)
    df["Resultados"] = df["Resultados"].astype(int)


def apresentar_relatorio(df, 
                         campanhas_selecionadas, 
                         data_inicial=pd.to_datetime("2019-01-01"), 
                         data_final=datetime.now(), 
                         mostrar_grafico=False):

    st.header(f":dart: {campanhas_selecionadas}")

    data_inicial = pd.to_datetime(data_inicial)
    data_final = pd.to_datetime(data_final)

    df = df.loc[(df["Dia"] >= data_inicial) & (df["Dia"] <= data_final)]
    df["Dia"] = df["Dia"].dt.date
    df["Início"] = df["Início"].dt.date
    
    plotly_chart = px.bar(df,
                          x = var_x, 
                          y = var_y, 
                          title=f"{var_y} x {var_x}",
                          barmode="group")
    
    if var_x != var_y:

        mostrar_grafico = True

    if mostrar_grafico == True:

        aba_grafico, aba_dados = st.tabs([":bar_chart: Gráfico", ":page_facing_up: Métricas"])

        aba_dados.dataframe(df)
        aba_grafico.plotly_chart(plotly_chart,
                            use_container_width=False, 
                            sharing="streamlit", 
                            theme="streamlit")
    else:

        st.dataframe(df)

st.set_page_config(
    layout="wide",
    page_title="Relatórios",
    page_icon=":chart_with_upwards_trend:"
    )

with st.sidebar:
    arquivo = st.file_uploader(
    label=":file_folder: Selecione um arquivo", 
    type="csv")

if arquivo is not None:

    df = pd.read_csv(
        arquivo,
        encoding="utf-8",
        )

    # Preparando dados
    df = df[["Dia",
        "Início",
        "Início dos relatórios",
        "Término",
        "Término dos relatórios",
        "Nome da campanha",
        "Nome do conjunto de anúncios",
        "Nome do anúncio",
        "Objetivo",
        "call_to_action_type",
        "Tipo de orçamento da campanha",
        "Orçamento da campanha",
        "Orçamento do conjunto de anúncios",
        "Valor usado (BRL)",
        "Idade",
        "Gênero",
        "Alcance",
        "Frequência",
        "Impressões",
        "Custo por 1.000 contas da Central de Contas alcançadas",
        "CPM (custo por 1.000 impressões)",
        "Públicos personalizados excluídos",
        "Públicos personalizados incluídos",
        "Tipo de resultado",
        "Resultados",
        "Custo por resultado",
        "Cliques no link únicos",
        "Custo por clique no link único",
        "CTR único (taxa de cliques no link)",
        "Classificação de qualidade",
        "Classificação da taxa de engajamento",
        "Classificação da taxa de conversão",
        "Engajamento com a Página",
        "Engajamentos com a publicação",
        "Reações à publicação",
        "Salvamentos da publicação",
        "Compartilhamentos da publicação",
        "Custo por engajamento com a Página",
        "Custo por engajamento com a publicação",
        "Reproduções do vídeo por no mínimo 3 segundos",
        "Reproduções de 25% do vídeo",
        "Reproduções de 50% do vídeo",
        "Reproduções de 75% do vídeo",
        "Reproduções de 95% do vídeo",
        "Tempo médio de reprodução do vídeo",
        "Reproduções de vídeo",
        "Custo por reprodução de vídeo por no mínimo 3 segundos",
        "ThruPlays",
        "Custo por ThruPlay",
        "Visitas ao perfil do Instagram"
        ]]

    tratar_dados_faltantes(df)
    tratar_tipos_dados(df)

    # Separando dados por objetivo de campanha

    #   Campanhas de Tráfego
    df_link_clicks = df[df["Objetivo"] == "LINK_CLICKS"]
    df_link_clicks = df_link_clicks[["Dia",
        "Início",
        "Nome da campanha",
        "Nome do conjunto de anúncios",
        "Nome do anúncio",
        "call_to_action_type",
        "Orçamento da campanha",
        "Valor usado (BRL)",
        "Idade",
        "Gênero",
        "Alcance",
        "Frequência",
        "Impressões",
        "Custo por 1.000 contas da Central de Contas alcançadas",
        "Públicos personalizados excluídos",
        "Públicos personalizados incluídos",
        "Visitas ao perfil do Instagram",
        "Cliques no link únicos",
        "Custo por clique no link único",
        "CTR único (taxa de cliques no link)"
        ]]
    df_link_clicks.sort_values(by="Dia", inplace=True)
    df_link_clicks.reset_index(inplace=True, drop=True)

    #   Campanhas de Engajamento
    df_outcome_engagement = df[df["Objetivo"] == "OUTCOME_ENGAGEMENT"]
    df_outcome_engagement = df_outcome_engagement[["Dia",
        "Início",
        "Nome da campanha",
        "Nome do conjunto de anúncios",
        "Nome do anúncio",
        "Objetivo",
        "call_to_action_type",
        "Orçamento da campanha",
        "Valor usado (BRL)",
        "Idade",
        "Gênero",
        "Alcance",
        "Frequência",
        "Impressões",
        "CPM (custo por 1.000 impressões)",
        "Públicos personalizados excluídos",
        "Públicos personalizados incluídos",
        "Tipo de resultado",
        "Resultados",
        "Custo por resultado",
        "Engajamento com a Página",
        "Engajamentos com a publicação",
        "Reações à publicação",
        "Salvamentos da publicação",
        "Compartilhamentos da publicação",
        "Custo por engajamento com a Página",
        "Custo por engajamento com a publicação"
        ]]
    df_outcome_engagement.sort_values(by="Dia", inplace=True)
    df_outcome_engagement.reset_index(inplace=True, drop=True)

    with st.sidebar:

        campanhas_selecionadas = st.radio(
            ":dart: Tipo de Campanha",
            ("Tráfego", "Engajamento"),
            label_visibility="visible")

        if campanhas_selecionadas == "Engajamento":

            df = df_outcome_engagement

        else:

            df = df_link_clicks

        data_inicial_padrao = df["Dia"].min()

        data_inicial_relatorio = st.date_input(
            ":calendar: Data - Inicial",
            value = data_inicial_padrao
        )
        data_final_relatorio = st.date_input(
            ":calendar: Data - Final",
            value = datetime.now()
        )

        var_x = st.selectbox(
            ":bar_chart: Gráfico - Eixo Horizontal",
            tuple(df.columns),
            label_visibility="visible")

        var_y = st.selectbox(
            ":bar_chart: Gráfico - Eixo Vertical",
            tuple(df.columns),
            label_visibility="visible")

    st.title(f"Meta Ads")

    apresentar_relatorio(
        df, 
        campanhas_selecionadas, 
        data_inicial = data_inicial_relatorio,
        data_final = data_final_relatorio)
