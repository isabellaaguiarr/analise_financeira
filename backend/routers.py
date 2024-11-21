import streamlit as st
import pandas as pd 
from backend.views import pegar_df_planilhao,filtrar_duplicado,pegar_df_preco_corrigido,pegar_df_preco_diversos, carteira

def menu_planilhao(data_base):
    # Chama a função para pegar os dados do Planilhão com base na data base.
    df = pegar_df_planilhao(data_base)
    return df

def menu_filtrar(data_base):
    # Chama a função remover as duplicadas.
    df_dupicado = filtrar_duplicado(data_base)
    return df_dupicado

def menu_estrategia(data, crit_rentabilidade, crit_desconto, num_acoes):
    # Chama a função para gerar a carteira com base nos critérios informados.
    df_estrategia = carteira(data, crit_rentabilidade, crit_desconto, num_acoes)
    return df_estrategia

def menu_preco_corrigido(ticker, data_ini, data_fim):
    # Chama a função para obter os preços corrigidos das ações para o período.
    df_precos_corrigidos = pegar_df_preco_corrigido(ticker, data_ini, data_fim)
    return df_precos_corrigidos

def menu_preco_diversos(ticker, data_ini, data_fim):
    # Chama a função para obter os preços diversos da ação  para o período.
    df_precos_diversos = pegar_df_preco_diversos(ticker, data_ini, data_fim)
    return df_precos_diversos

