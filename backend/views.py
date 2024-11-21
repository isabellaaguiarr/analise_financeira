import pandas as pd
from datetime import date
import logging
logger = logging.getLogger(__name__)
from backend.apis import (pegar_planilhao, get_preco_corrigido, get_preco_diversos)

def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido (defau

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume)

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]
    lst_dup = df_dup.empresa.unique()
    lst_final = []
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
        lst_final = lst_final + [tic_dup]
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)]

def pegar_df_planilhao(data_base:date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações.
    """
    dados = pegar_planilhao(data_base)
    if dados:
        dados = dados['dados']
        planilhao = pd.DataFrame(dados)
        planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
        df = filtrar_duplicado(planilhao)
        logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
        print(f"Dados do Planilhao consultados com sucesso: {data_base}")
        return df
    else:
        logger.info(f"Sem Dados no Planilhão: {data_base}")
        print(f"Sem Dados no Planilhão: {data_base}")

def carteira(data, crit_rentabilidade, crit_desconto, num_acoes):
    df = pegar_df_planilhao(data)
    colunas_relevantes = ["ticker", "setor", "data_base", "roc", "roe", "roic", "earning_yield", "dividend_yield", "p_vp"]
    df = df[colunas_relevantes]
    
    # Seleção com base na rentabilidade (usando todas as ações disponíveis)
    df_rentabilidade = df.nlargest(len(df), crit_rentabilidade).reset_index(drop=True)
    df_rentabilidade['rank_rentabilidade'] = df_rentabilidade.index  
    
    # Seleção com base no desconto (ajustando a seleção para o critério 'p_vp')
    if crit_desconto == "p_vp":
        df_desconto = df.nsmallest(len(df), crit_desconto).reset_index(drop=True)
    else:
        df_desconto = df.nlargest(len(df), crit_desconto).reset_index(drop=True)
    df_desconto['rank_desconto'] = df_desconto.index 
    
    # Combinação dos DataFrames e cálculo da média dos rankings
    df_combinado = pd.merge(df_desconto[["ticker", "rank_desconto"]], 
                            df_rentabilidade[["ticker", "rank_rentabilidade", "roc", "earning_yield"]], 
                            on="ticker", 
                            how="inner")
    df_combinado["pontuacao_media"] = (df_combinado["rank_desconto"] + df_combinado["rank_rentabilidade"]) / 2
    
    # Ordenação e seleção das melhores ações com ranking iniciado em 1
    df_ordenado = df_combinado.sort_values(by=['pontuacao_media'], ascending=True).reset_index(drop=True)
    df_ordenado['rank_final'] = df_ordenado.index + 1  # Adiciona ranking final começando em 1
    df_final = df_ordenado.nsmallest(num_acoes, 'pontuacao_media').reset_index(drop=True)
    
    return df_final[['ticker', 'roc', 'earning_yield', 'rank_rentabilidade', 'rank_desconto', 'rank_final']]

def pegar_df_preco_corrigido(data_ini: date, data_fim: date, carteira: list) -> pd.DataFrame:
    """
    Consulta os preços corrigidos de uma lista de ações
    """
    df_preco_corrigido = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_corrigido(ticker, data_ini, data_fim)
        if dados and 'dados' in dados:  # Verifica se 'dados' existe no retorno
            df_temp = pd.DataFrame.from_dict(dados['dados'])
            df_preco_corrigido= pd.concat([df_preco_corrigido, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco_corrigido

def pegar_df_preco_diversos(data_ini: date, data_fim: date, carteira: list) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma carteira de ativos
    """
    df_preco_diversos = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_diversos(ticker, data_ini, data_fim)
        if dados and 'dados' in dados:  # Verifica se 'dados' existe no retorno
            df_temp = pd.DataFrame.from_dict(dados['dados'])
            df_preco = pd.concat([df_preco_diversos, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')
        else:
            logger.error(f"Sem Preco diversos: {ticker}")
            print(f"Sem Preco diversos: {ticker}")
    return df_preco_diversos



