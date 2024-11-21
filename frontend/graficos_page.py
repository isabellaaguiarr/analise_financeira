import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from backend.apis import get_preco_diversos, get_preco_corrigido  

st.title("Análise da Carteira")
aba_selecionada = st.radio(
    "Escolha o que deseja visualizar:",
    ["Gráficos individuais", "Análise Comparativa"] 
)

if "carteira_df" in st.session_state:
    carteira_df = st.session_state["carteira_df"]

    if aba_selecionada == "Gráficos individuais":
        if "ticker" in carteira_df.columns and "rank_final" in carteira_df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(carteira_df["ticker"], carteira_df["rank_final"], color="skyblue")
            ax.set_xlabel("Ticker da Ação")
            ax.set_ylabel("Rank Final")
            ax.set_title("Gráfico de Rank Final das Ações")
            st.pyplot(fig)

            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.bar(carteira_df["ticker"], carteira_df["rank_desconto"], color="lightcoral")
            ax2.set_xlabel("Ticker da Ação")
            ax2.set_ylabel("Rank Desconto")
            ax2.set_title("Gráfico de Rank Desconto das Ações")
            st.pyplot(fig2)

            fig3, ax3 = plt.subplots(figsize=(10, 6))
            ax3.bar(carteira_df["ticker"], carteira_df["rank_rentabilidade"], color="lightgreen")
            ax3.set_xlabel("Ticker da Ação")
            ax3.set_ylabel("Rank Rentabilidade")
            ax3.set_title("Gráfico de Rank Rentabilidade das Ações")
            st.pyplot(fig3)
        
        else:
            st.error("Colunas 'ticker', 'rank_final', 'rank_rentabilidade' ou 'rank_desconto' não encontradas no DataFrame.")
    
    elif aba_selecionada == "Análise Comparativa":
        st.sidebar.title("Configurações")
        st.session_state["data_ini"] = st.sidebar.date_input(
            "Data de Início", 
            st.session_state.get("data_ini", pd.to_datetime("2023-04-04"))
        )
        st.session_state["data_fim"] = st.sidebar.date_input(
            "Data de Fim", 
            st.session_state.get("data_fim", pd.to_datetime("2024-04-01"))
        )

        df_ibov = get_preco_diversos("IBOV", st.session_state["data_ini"], st.session_state["data_fim"])

        if df_ibov is not None and 'dados' in df_ibov:
            df_ibov = pd.DataFrame(df_ibov['dados'])
            df_ibov['fechamento_normalizado'] = df_ibov['fechamento'] / df_ibov['fechamento'].iloc[0]
        else:
            st.warning("Não foi possível obter dados do IBOV.")
            df_ibov = pd.DataFrame()

        if not carteira_df.empty:
            df_acao_carteira = pd.DataFrame()

            for ticker in carteira_df["ticker"]:
                st.write(f"Consultando dados para o ticker: {ticker}")
                df_temp = get_preco_corrigido(ticker, st.session_state["data_ini"], st.session_state["data_fim"])

                if df_temp is not None and 'dados' in df_temp:
                    df_temp = pd.DataFrame(df_temp['dados'])
                    df_temp['ticker'] = ticker
                    df_temp['fechamento_normalizado'] = df_temp['fechamento'] / df_temp['fechamento'].iloc[0]
                    df_acao_carteira = pd.concat([df_acao_carteira, df_temp], axis=0)
                else:
                    st.warning(f"Não foi possível obter dados para o ticker: {ticker}")

            if not df_acao_carteira.empty and not df_ibov.empty:
                st.write("Dados carregados com sucesso!")
                fig4, ax4 = plt.subplots(figsize=(12, 6))

                for ticker in carteira_df["ticker"]:
                    df_ticker = df_acao_carteira[df_acao_carteira['ticker'] == ticker]
                    ax4.plot(df_ticker['data'], df_ticker['fechamento_normalizado'], label=f'{ticker}')

                ax4.plot(df_ibov['data'], df_ibov['fechamento_normalizado'], label="IBOV", color='black', linestyle='--')

                # Formatação do eixo X para exibir apenas dia/mês
                ax4.set_xlabel("Data")
                ax4.set_ylabel("Preço Normalizado")
                ax4.set_title("Comparação entre Carteira e IBOV")
                ax4.legend()
                ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Exibe um mês por tick
                ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))  # Formata para DD/MM - DATA/MÊS
                fig4.autofmt_xdate()  

                st.pyplot(fig4)
            else:
                st.error("Não foi possível obter dados suficientes para plotar o gráfico.")

else:
    st.write("Nenhuma carteira gerada. Execute a estratégia primeiro.")
