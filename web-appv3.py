import streamlit as st
import os
import glob
import pandas as pd
import datetime
from datetime import datetime
import locale
import zipfile
from atualizacao_contratos_ap007a import *
from atualizacao_contratos_ap007b import *
from atualizacao_optin_agenda_ap004 import *
from criacao_contratos_ap007a import *
from criacao_contratos_ap007b import *
from criacao_optin_agenda_ap004 import *
from inativacao_contratos_pagos import *
from inativacao_contratos_ap007a import *
from inativacao_contratos_ap007b import *
from inativacao_optin_agenda_ap006 import *
from processar_arquivos_ap007a import *
from processar_arquivos_ap007b import *
from processar_cnpj_cobranca import *
from processar_pagamentos import * 
from processar_um_arquivo_ap007a import *
from processar_extratos_bancarios import *


# Configurar o locale para formato brasileiro
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
#locale.setlocale(locale.LC_ALL, 'pt_BR')
#locale.setlocale(locale.LC_ALL, os.getenv("LC_ALL", "C.UTF-8"))
try:
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_MONETARY, 'C.UTF-8')  # Fallback para evitar erro
# from functions import *
#from backend import corrigir_valor, consolidar_arquivos_ap007b, processar_arquivos_ap007a, processar_dados_cobranca, gerar_arquivo_ap007a_criacao, gerar_arquivo_ap007a_atualizacao, gerar_arquivo_ap007a_inativacao, gerar_arquivo_ap007b_criacao, gerar_arquivo_ap007b_atualizacao, gerar_arquivo_ap007b_inativacao, processar_casos_de_inativacao, carregar_dados_cobranca_relatorio_final_marketup, gerar_relatorio_final_marketup

# Usado para salvar e encontrar os arquivos do dia
data_nome_arquivo = datetime.now().strftime('%Y%m%d')
data_atual = datetime.now().strftime("%d_%m_%Y")

# CONFIGURAÇÕES DE DATAS 
# Obtém o mês atual
mes_atual = datetime.now()

# Cria uma lista com os prefixos dos meses
prefixos_meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

# Usa o número do mês para obter o prefixo correspondente
prefixo_mes = prefixos_meses[mes_atual.month - 1]

# Formatação monetária sem 'locale'   
def format_currency(value):
    if pd.notnull(value):
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "0,00"   

# Função para obter o caminho da pasta
def obter_caminho_pasta(file):
    if file is not None:
        return os.path.dirname(file.name)
    return None

# Estilo CSS para centralizar horizontalmente
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
    }
    .stButton button {
        width: 700px;
        height: 50px;
        font-size: 16px;
        margin: 10px;
    }
    .title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        white-space: nowrap; /* Evita quebra de linha */
    }
    .subtitle {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        white-space: nowrap; /* Evita quebra de linha */
    </style>
    """, unsafe_allow_html=True)

# Inicializar a variável de estado
if "page" not in st.session_state:
    st.session_state.page = "home"  # Página inicial

# Funções para cada página
def home():
    st.markdown('<div class="title">Bem-vindo(a) ao criador de relatórios VEON</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    if st.button("Relatório de Contratos CERC"):
        st.session_state.page = "menu_tipo_relatorio"
        #st.session_state.page = "menu_relatorio_cerc"
    if st.button("Relatório MarketUP"):
        st.session_state.page = "menu_relatorio_marketup"
    # if st.button("Relatório Financeiro"):
    #     st.session_state.page = "menu_relatorio_financeiro"
    if st.button("Extratos Bancários"):
        st.session_state.page = "menu_extratos_bancarios"
    st.markdown('</div>', unsafe_allow_html=True)
    
def menu_tipo_relatorio():
    st.markdown('<div class="title">Qual o tipo do relatório?</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    #if st.button("CERC-AP004"):
       # st.session_state.page = "ap004"
    if st.button("CERC-AP007A / CERC-AP007B"):
        st.session_state.page = "ap007a_ap007b"
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Voltar"):
        st.session_state.page = "home"
    
def menu_relatorio_cerc():
    st.markdown('<div class="title">Relatório de Contratos CERC</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Escolha o tipo da operação</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    if st.button("Criação de contratos CERC"):
        st.session_state.page = "criacao_contratos"
    if st.button("Atualização de contratos CERC"):
        st.session_state.page = "atualizacao_contratos"
    if st.button("Inativação de contratos CERC"):
        st.session_state.page = "inativacao_contratos"
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Voltar"):
        st.session_state.page = "home"
 
###################### CRIAÇÃO DE AGENDA OPT-IN ################################

def criacao_agenda():
    st.markdown('<div class="title">Criação de Agendas OPT-IN CERC</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    
    def fluxo_processamento_criacao_agenda():
        # Define variáveis na sessão para armazenar os inputs dos usuários
        if "df_ap007b_ret" not in st.session_state:
            st.session_state.df_ap007b_ret = None
        if "df_cnpj" not in st.session_state:
            st.session_state.df_cnpj = None

        # Input para o caminho da pasta AP007B
        st.markdown('<div class="subtitle">Insira o caminho da pasta com os arquivos AP007B</div>', unsafe_allow_html=True)
        path_ap007b = st.text_input("Digite o caminho da pasta (AP007B):")

        # Input para o caminho do arquivo de cobrança
        st.markdown('<div class="subtitle">Insira o caminho do arquivo de cobrança</div>', unsafe_allow_html=True)
        path_cobranca = st.text_input("Digite o caminho do arquivo (Cobrança):")

        # Input para datas de início e fim da assinatura
        st.markdown('<div class="subtitle">Insira a data de início da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
        data_inicio_assinatura = st.text_input("Data de início da assinatura:")

        st.markdown('<div class="subtitle">Insira a data de fim da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
        data_fim_assinatura = st.text_input("Data de fim da assinatura:")

        # Input para o número do arquivo
        st.markdown('<div class="subtitle">Insira o número deste arquivo</div>', unsafe_allow_html=True)
        numero_arquivo = st.text_input("Número do arquivo:")

        # Botão para processar tudo
        if st.button("Processar Tudo"):
            # Verifica se todos os campos foram preenchidos
            if path_ap007b and path_cobranca and data_inicio_assinatura and data_fim_assinatura and numero_arquivo:
                # Processa os arquivos com base nos inputs fornecidos
                df_ap007b_ret = processar_arquivos_ap007b(path_ap007b)
                df_cnpj = processar_cnpj_cobranca(path_cobranca, df_ap007b_ret)
                
                # Gerando arquivo AP007A
                gerar_arquivo_ap004_criacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                                
                # Mensagens ao usuário
                st.markdown('<div class="subtitle">Arquivo AP004 gerado com sucesso!</div>', unsafe_allow_html=True)

            else:
                st.warning("Por favor, preencha todos os campos antes de processar.")

    fluxo_processamento_criacao_agenda()
    
    if st.button("Voltar"):
        st.session_state.page = "menu_tipo_relatorio"        
        
def atualizacao_agenda():
    st.markdown('<div class="title">Atualização de Agenda OPT-IN CERC</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    
    def fluxo_processamento_atualizacao_agenda():
            # Armazenar o estado das etapas
            if "consultado" not in st.session_state:
                st.session_state.consultado = False
            if "continuar" not in st.session_state:
                st.session_state.continuar = False
            # Define variáveis na sessão para armazenar os inputs dos usuários
            if "df_ap007b_ret" not in st.session_state:
                st.session_state.df_ap007b_ret = None
            if "df_cnpj" not in st.session_state:
                st.session_state.df_cnpj = None

            # Caminho dos arquivos de retorno, nesta etapa processamos todos os arquivos
            path_ap007b = 'C:/Users/Vítor/Documents/VEON/arquivos_retorno/arquivos_ap007b'

            # Input para o caminho do arquivo de cobrança
            st.markdown('<div class="subtitle">Insira o caminho do arquivo de cobrança</div>', unsafe_allow_html=True)
            path_cobranca = st.text_input("Digite o caminho do arquivo (Cobrança):")
            
            # Input para o caminho do arquivo AP007A
            st.markdown('<div class="subtitle">Insira o caminho do arquivo AP004</div>', unsafe_allow_html=True)
            path_ap007a = st.text_input("Digite o caminho do arquivo (AP004):")
            
            # Botão para consultar os arquivos
            if st.button("Consultar"):
                if path_ap007b and path_cobranca and path_ap007a:
                    df_ap007b_ret = processar_arquivos_ap007b(path_ap007b)
                    df_cnpj = processar_cnpj_cobranca(path_cobranca, df_ap007b_ret)
                    df_ap007a_ret, df_onerados, df_reenviar, df_erros = processar_um_arquivo_ap007a(path_ap007a, df_cnpj)
                    
                    onerados = df_onerados.shape[0]
                    atualizar = df_reenviar.shape[0]
                    erros = df_erros.shape[0]
                    
                    st.write(f'Foram encontrados {onerados} URs oneradas, {atualizar} para atualizar e {erros} deram erro')
                    
                    # Define o estado como consultado para mostrar o botão "Continuar"
                    st.session_state.consultado = True
                    
            # Botão de "Continuar" para avançar para as próximas etapas
            if st.session_state.consultado:
                if st.button("Continuar"):
                    st.session_state.continuar = True

            if st.session_state.continuar:
                # Input para datas de início e fim da assinatura
                st.markdown('<div class="subtitle">Insira a data de início da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
                data_inicio_assinatura = st.text_input("Data de início da assinatura:")

                st.markdown('<div class="subtitle">Insira a data de fim da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
                data_fim_assinatura = st.text_input("Data de fim da assinatura:")

                # Input para o número do arquivo
                st.markdown('<div class="subtitle">Insira o número deste arquivo</div>', unsafe_allow_html=True)
                numero_arquivo = st.text_input("Número do arquivo:")

                # Botão para processar tudo
                if st.button("Processar Tudo"):
                    # Verifica se todos os campos foram preenchidos
                    if path_ap007b and path_cobranca and data_inicio_assinatura and data_fim_assinatura and numero_arquivo:
                        # Processa os arquivos com base nos inputs fornecidos
                        df_ap007b_ret = processar_arquivos_ap007b(path_ap007b)
                        df_cnpj = processar_cnpj_cobranca(path_cobranca, df_ap007b_ret)
                        
                        # Exibe mensagens de sucesso e/ou dados processados
                        st.write("Processamento completo!")
                        st.write("Arquivos AP007B e cobrança processados com sucesso!")
                        
                        # Gerando arquivo AP007A
                        gerar_arquivo_ap007a_atualizacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                                        
                        # Mensagens ao usuário
                        st.markdown('<div class="subtitle">Arquivo AP007A gerado com sucesso!</div>', unsafe_allow_html=True)
                            
                        # Gerando arquivo AP007B
                        gerar_arquivo_ap007b_atualizacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                                        
                        # Mensagens ao usuário
                        st.markdown('<div class="subtitle">Arquivo AP007B gerado com sucesso!</div>', unsafe_allow_html=True)

                    else:
                        st.warning("Por favor, preencha todos os campos antes de processar.")

    fluxo_processamento_atualizacao_agenda()
    
    if st.button("Voltar"):
        st.session_state.page = "menu_tipo_relatorio"        
        
###################### CRIAÇÃO DOS CONTRATOS ###################################        
def criacao_contratos():
    st.markdown('<div class="title">Criação de contratos CERC</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    
    def fluxo_processamento_criacao():
        # Define variáveis na sessão para armazenar os inputs dos usuários
        if "df_ap007b_ret" not in st.session_state:
            st.session_state.df_ap007b_ret = None
        if "df_cnpj" not in st.session_state:
            st.session_state.df_cnpj = None

        # Input para o caminho da pasta AP007B
        # st.markdown('<div class="subtitle">Insira o caminho da pasta com os arquivos AP007B</div>', unsafe_allow_html=True)
        # path_ap007b = st.text_input("Digite o caminho da pasta (AP007B):")
        
        path_ap007b = st.file_uploader("Faça o upload dos arquivos AP007B", accept_multiple_files=True, type="csv")

        # Input para o caminho do arquivo de cobrança
        # st.markdown('<div class="subtitle">Insira o caminho do arquivo de cobrança</div>', unsafe_allow_html=True)
        # path_cobranca = st.text_input("Digite o caminho do arquivo (Cobrança):")
        
        path_cobranca = st.file_uploader("Faça o upload do arquivo de CNPJ da Marketup", accept_multiple_files=False, type="xlsx")

        # Input para datas de início e fim da assinatura
        #st.markdown('<div class="subtitle">Insira a data de início da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
        #data_inicio_assinatura = st.text_input("Data de início da assinatura:")
        data_inicio_assinatura = st.date_input("Data de início da assinatura", 
                                               value=None,
                                               format="YYYY-MM-DD")

        #st.markdown('<div class="subtitle">Insira a data de fim da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
        #data_fim_assinatura = st.text_input("Data de fim da assinatura:")
        data_fim_assinatura = st.date_input("Data final da assinatura", 
                                               value=None,
                                               format="YYYY-MM-DD")

        # Input para o número do arquivo
        st.markdown('<div class="subtitle">Insira o número deste arquivo</div>', unsafe_allow_html=True)
        numero_arquivo = st.text_input("Número do arquivo:")

        # Botão para processar tudo
        if st.button("Processar Tudo"):
            # Verifica se todos os campos foram preenchidos
            if path_ap007b and path_cobranca and data_inicio_assinatura and data_fim_assinatura and numero_arquivo:
                # Processa os arquivos com base nos inputs fornecidos
                df_ap007b_ret = processar_arquivos_ap007b(path_ap007b)
                df_cnpj = processar_cnpj_cobranca(path_cobranca, df_ap007b_ret)
                
                # Exibe mensagens de sucesso e/ou dados processados
                st.write("Processamento completo!")
                
                # Gerando arquivo AP007A
                buffer_a, nome_arquivo_a = gerar_arquivo_ap007a_criacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                
                st.session_state['buffer_a'] = buffer_a
                st.session_state['nome_arquivo_a'] = nome_arquivo_a
                                
                    
                # Gerando arquivo AP007B
                buffer_b, nome_arquivo_b = gerar_arquivo_ap007b_criacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                
                st.session_state['buffer_b'] = buffer_b
                st.session_state['nome_arquivo_b'] = nome_arquivo_b
                                

            else:
                st.warning("Por favor, preencha todos os campos antes de processar.")
                
            # Verificar se os arquivos foram processados e se o botão "Processar Tudo" foi clicado
            if 'buffer_a' in st.session_state and 'buffer_b' in st.session_state:
                # Criar um arquivo ZIP com os dois arquivos CSV
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    zf.writestr(f"{st.session_state['nome_arquivo_a']}.gz", st.session_state['buffer_a'].getvalue())
                    zf.writestr(f"{st.session_state['nome_arquivo_b']}.gz", st.session_state['buffer_b'].getvalue())
                zip_buffer.seek(0)

                # Adicionar botão de download para o arquivo ZIP
                st.download_button(
                    label="Baixar arquivos AP007A e AP007B",
                    data=zip_buffer,
                    file_name="arquivos.zip",
                    mime="application/zip"
                )

    fluxo_processamento_criacao()
    
    if st.button("Voltar"):
        st.session_state.page = "home"
        
def atualizacao_contratos():
    st.markdown('<div class="title">Atualização de contratos CERC</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    
    def fluxo_processamento_atualizacao():
            # Armazenar o estado das etapas
            if "consultado" not in st.session_state:
                st.session_state.consultado = False
            if "continuar" not in st.session_state:
                st.session_state.continuar = False
            # Define variáveis na sessão para armazenar os inputs dos usuários
            if "df_ap007b_ret" not in st.session_state:
                st.session_state.df_ap007b_ret = None
            if "df_cnpj" not in st.session_state:
                st.session_state.df_cnpj = None

            # Caminho dos arquivos de retorno, nesta etapa processamos todos os arquivos
            path_ap007b = st.file_uploader("Faça o upload dos arquivos AP007B", accept_multiple_files=True, type="csv")

            # Input para o caminho do arquivo de cobrança
            #st.markdown('<div class="subtitle">Insira o caminho do arquivo de cobrança</div>', unsafe_allow_html=True)
            path_cobranca = st.file_uploader("Faça o upload do arquivo de CNPJ da Marketup", accept_multiple_files=False, type="xlsx")
            
            # Input para o caminho do arquivo AP007A
            #st.markdown('<div class="subtitle">Insira o caminho do arquivo AP007A</div>', unsafe_allow_html=True)
            path_ap007a = st.file_uploader("Faça o upload do arquivo AP007A", accept_multiple_files=False, type="csv")
            
            # Botão para consultar os arquivos
            if st.button("Consultar"):
                if path_ap007b and path_cobranca and path_ap007a:
                    df_ap007b_ret = processar_arquivos_ap007b(path_ap007b)
                    df_cnpj = processar_cnpj_cobranca(path_cobranca, df_ap007b_ret)
                    df_ap007a_ret, df_onerados, df_reenviar, df_erros = processar_um_arquivo_ap007a(path_ap007a, df_cnpj)
                    
                    onerados = df_onerados.shape[0]
                    atualizar = df_reenviar.shape[0]
                    erros = df_erros.shape[0]
                    
                    st.write(f'Foram encontrados {onerados} URs oneradas, {atualizar} para atualizar e {erros} deram erro')
                    
                    # Define o estado como consultado para mostrar o botão "Continuar"
                    st.session_state.consultado = True
                    
            # Botão de "Continuar" para avançar para as próximas etapas
            if st.session_state.consultado:
                if st.button("Continuar"):
                    st.session_state.continuar = True

            if st.session_state.continuar:
                # Input para datas de início e fim da assinatura
                #st.markdown('<div class="subtitle">Insira a data de início da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
                data_inicio_assinatura = st.date_input("Data de inicío da assinatura", 
                                               value=None,
                                               format="YYYY-MM-DD")

                #st.markdown('<div class="subtitle">Insira a data de fim da assinatura (YYYY-MM-DD):</div>', unsafe_allow_html=True)
                data_fim_assinatura = st.date_input("Data final da assinatura", 
                                               value=None,
                                               format="YYYY-MM-DD")

                # Input para o número do arquivo
                st.markdown('<div class="subtitle">Insira o número deste arquivo</div>', unsafe_allow_html=True)
                numero_arquivo = st.text_input("Número do arquivo:")

                # Botão para processar tudo
                if st.button("Processar Tudo"):
                    # Verifica se todos os campos foram preenchidos
                    if path_ap007b and path_cobranca and data_inicio_assinatura and data_fim_assinatura and numero_arquivo:
                        # Processa os arquivos com base nos inputs fornecidos
                        df_ap007b_ret = processar_arquivos_ap007b(path_ap007b)
                        df_cnpj = processar_cnpj_cobranca(path_cobranca, df_ap007b_ret)
                        
                        # Exibe mensagens de sucesso e/ou dados processados
                        st.write("Processamento completo!")
                        #st.write("Arquivos AP007B e cobrança processados com sucesso!")
                        
                        # Gerando arquivo AP007A
                        buffer_a, nome_arquivo_a = gerar_arquivo_ap007a_atualizacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                        
                        st.session_state['buffer_a'] = buffer_a
                        st.session_state['nome_arquivo_a'] = nome_arquivo_a
                                        
                        # Mensagens ao usuário
                        #st.markdown('<div class="subtitle">Arquivo AP007A gerado com sucesso!</div>', unsafe_allow_html=True)
                            
                        # Gerando arquivo AP007B
                        buffer_b, nome_arquivo_b = gerar_arquivo_ap007b_atualizacao(df_cnpj, prefixo_mes=prefixo_mes, data_nome_arquivo=datetime.now().strftime('%Y%m%d'), data_inicio_assinatura=data_inicio_assinatura, data_fim_assinatura=data_fim_assinatura, numero_arquivo=numero_arquivo)
                        
                        st.session_state['buffer_b'] = buffer_b
                        st.session_state['nome_arquivo_b'] = nome_arquivo_b
                                        
                        # Mensagens ao usuário
                        #st.markdown('<div class="subtitle">Arquivo AP007B gerado com sucesso!</div>', unsafe_allow_html=True)

                    else:
                        st.warning("Por favor, preencha todos os campos antes de processar.")
                        
                    # Verificar se os arquivos foram processados e se o botão "Processar Tudo" foi clicado
                    if 'buffer_a' in st.session_state and 'buffer_b' in st.session_state:
                        # Criar um arquivo ZIP com os dois arquivos CSV
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w") as zf:
                            zf.writestr(f"{st.session_state['nome_arquivo_a']}.gz", st.session_state['buffer_a'].getvalue())
                            zf.writestr(f"{st.session_state['nome_arquivo_b']}.gz", st.session_state['buffer_b'].getvalue())
                        zip_buffer.seek(0)

                        # Adicionar botão de download para o arquivo ZIP
                        st.download_button(
                            label="Baixar arquivos AP007A e AP007B",
                            data=zip_buffer,
                            file_name="arquivos.zip",
                            mime="application/zip"
                        )

    fluxo_processamento_atualizacao()
    
    if st.button("Voltar"):
        st.session_state.page = "home"
        
def inativacao_contratos():
    st.markdown('<div class="title">Inativação de contratos CERC</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    
    def fluxo_processamento_inativacao():
            
        # Define variáveis na sessão para armazenar os inputs dos usuários
        if "df_ap007b_ret" not in st.session_state:
            st.session_state.df_ap007b_ret = None
        if "df_cnpj" not in st.session_state:
            st.session_state.df_cnpj = None
        
        # Caminho do arquivo que possui os CNPJs pagos que devem ser inativados
        path_inativacao = st.file_uploader("Faça o upload do arquivo com os CNPJs para inativação", accept_multiple_files=False, type="xlsx")
        
        # Caminho dos arquivos de retorno, nesta etapa processamos todos os arquivos
        path_ap007b = st.file_uploader("Faça o upload do arquivo AP007A", accept_multiple_files=False)
        
        # Caminho dos arquivos de retorno AP007A
        path_ap007a = st.file_uploader("Faça o upload do arquivo AP007B", accept_multiple_files=False)
        
        # Input para o número do arquivo
        st.markdown('<div class="subtitle">Insira o número deste arquivo</div>', unsafe_allow_html=True)
        numero_arquivo = st.text_input("Número do arquivo:")
        
        
        # Botão para processar tudo
        if st.button("Processar Tudo"):
            # Verifica se todos os campos foram preenchidos
            if path_inativacao and path_ap007b and path_ap007a and numero_arquivo:
                # Processa os arquivos com base nos inputs fornecidos
                buffer_ap007a, nome_arquivo_ap007a, buffer_ap007b, nome_arquivo_ap007b = gerar_arquivos_inativacao(path_ap007a, path_ap007b, path_inativacao, data_nome_arquivo, numero_arquivo)
                
                st.session_state['buffer_ap007a'] = buffer_ap007a
                st.session_state['buffer_ap007b'] = buffer_ap007b
                st.session_state['nome_arquivo_ap007a'] = nome_arquivo_ap007a
                st.session_state['nome_arquivo_ap007b'] = nome_arquivo_ap007b

            else:
                st.warning("Por favor, preencha todos os campos antes de processar.")
        
            # Verificar se os arquivos foram processados e se o botão "Processar Tudo" foi clicado
            if 'buffer_ap007a' in st.session_state and 'buffer_ap007b' in st.session_state:
                # Criar um arquivo ZIP com os dois arquivos CSV
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    zf.writestr(f"{st.session_state['nome_arquivo_ap007a']}.gz", st.session_state['buffer_ap007a'].getvalue())
                    zf.writestr(f"{st.session_state['nome_arquivo_ap007b']}.gz", st.session_state['buffer_ap007b'].getvalue())
                zip_buffer.seek(0)

                # Adicionar botão de download para o arquivo ZIP
                st.download_button(
                    label="Baixar arquivos de inativação AP007A e AP007B",
                    data=zip_buffer,
                    file_name="arquivos.zip",
                    mime="application/zip"
                )
            
    fluxo_processamento_inativacao()
    
    if st.button("Voltar"):
        st.session_state.page = "home"

def menu_relatorio_marketup():
    st.markdown('<div class="title">Relatório MarketUP</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    st.markdown('<div class="subtitle">Arquivos de Entrada</div>', unsafe_allow_html=True)
    
    # Verifica se os dados já foram processados
    if 'resultado_final' not in st.session_state:
        st.session_state.resultado_final = None

    uploaded_ap005_files = st.file_uploader("Selecione os arquivos AP005", 
                                          type=['csv', 'xlsx'], 
                                          accept_multiple_files=True)
    uploaded_cnpj = st.file_uploader("Selecione o arquivo de CNPJs da Marketup", 
                                    type=['csv', 'xlsx'])

    # Adiciona checkbox para ativar filtros de data
    enable_date_filter = st.checkbox("Ativar filtros de data?")
    
    # Inicializa as variáveis de data
    start_date = None
    end_date = None
    
    # Se o checkbox estiver marcado, mostra os seletores de data
    if enable_date_filter:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data de início", 
                                     value=None,
                                     format="YYYY-MM-DD")
        with col2:
            end_date = st.date_input("Data final",
                                   value=None,
                                   format="YYYY-MM-DD")
        
        if start_date and end_date and start_date > end_date:
            st.error("A data de início deve ser anterior à data final!")
            return

    if st.button("Processar Arquivos"):
        if not uploaded_ap005_files or uploaded_cnpj is None:
            st.error("Por favor, faça upload de pelo menos um arquivo AP005 e o arquivo de CNPJs agrupados")
            return
        try:
            # Adiciona barra de progresso e texto de status
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Lendo arquivo de CNPJs
            status_text.text("Lendo arquivo de CNPJs...")
            if uploaded_cnpj.name.endswith('.xlsx'):
                df_cnpj = pd.read_excel(uploaded_cnpj)
            else:
                df_cnpj = pd.read_csv(uploaded_cnpj, delimiter=';')

            # Processando arquivos AP005
            batch_size = 10
            all_ap005_dfs = []
            total_files = len(uploaded_ap005_files)
            
            for i in range(0, total_files, batch_size):
                batch_files = uploaded_ap005_files[i:i + batch_size]
                
                for idx, ap005_file in enumerate(batch_files):
                    try:
                        status_text.text(f"Processando arquivo {i + idx + 1} de {total_files}...")
                        progress_bar.progress((i + idx + 1) / total_files)
                        
                        if ap005_file.name.endswith('.xlsx'):
                            df = pd.read_excel(ap005_file)
                        else:
                            df = pd.read_csv(ap005_file, delimiter=';')
                        
                        # Limpando memória dos arquivos
                        ap005_file.seek(0)
                        
                        # Processando colunas
                        num_colunas = len(df.columns)
                        colunas_base = [
                            "referencia_externa", "entidade_registradora", 
                            "instituicao_credenciadora", "usuario_final_recebedor", 
                            "arranjo_pagamento", "data_liquidacao",
                            "titular_unidade_recebivel", "constituicao_unidade_recebivel", 
                            "valor_constituido_total", "valor_constituido_antecipacao_pre_contratado", 
                            "valor_bloqueado", "informacoes_pagamento", "carteira", 
                            "valor_livre", "valor_total_ur", "dt_atualizacao_ur"
                        ]
                        
                        if num_colunas > len(colunas_base):
                            colunas_extras = [f"coluna_{i}" for i in range(len(colunas_base), num_colunas)]
                            colunas = colunas_base + colunas_extras
                        else:
                            colunas = colunas_base[:num_colunas]
                        
                        df.columns = colunas
                        
                        # Se o filtro de data estiver ativo, aplica o filtro
                        if enable_date_filter and start_date and end_date:
                            # Processa a coluna 12 (informacoes_pagamento) para extrair a data
                            if 'data_liquidacao' in df.columns:
                                df['data_liquidacao'] = pd.to_datetime(df['data_liquidacao'], errors='coerce')
                            else:
                                st.warning(f"O arquivo {ap005_file.name} não contém a coluna 'data_liquidacao'. Será ignorado.")
                                continue  # Ignora arquivos sem essa coluna

                            # Filtra apenas os registros dentro do período especificado
                        if enable_date_filter and start_date and end_date:
                            mask = (df['data_liquidacao'] >= pd.Timestamp(start_date)) & \
                                (df['data_liquidacao'] <= pd.Timestamp(end_date))
                            df = df[mask]

                        
                        colunas_necessarias = [col for col in colunas_base if col in df.columns]
                        df = df[colunas_necessarias]
                        
                        all_ap005_dfs.append(df)
                        
                        # Limpando memória
                        del df
                        
                    except Exception as e:
                        st.warning(f"Erro ao processar arquivo {ap005_file.name}: {str(e)}")
                        continue

            status_text.text("Combinando dados...")
             # Combinando DataFrames
            if all_ap005_dfs:
                combined_ap005 = pd.concat(all_ap005_dfs, ignore_index=True)
                combined_ap005 = combined_ap005.drop_duplicates()

                # Limpando memória
                del all_ap005_dfs

                status_text.text("Processando resultados...")
                resultado_final = process_payment_data(combined_ap005, df_cnpj)
                
                # Armazena o resultado no session_state
                st.session_state.resultado_final = resultado_final

                st.success("Processamento concluído com sucesso!")
                
                # Adiciona informação sobre o período filtrado
                if enable_date_filter and start_date and end_date:
                    st.info(f"Dados filtrados para o período de {start_date.strftime('%d/%m/%Y')} "
                           f"até {end_date.strftime('%d/%m/%Y')}")
                
            else:
                st.error("Nenhum dado foi encontrado após o processamento dos arquivos.")

        except Exception as e:
            st.error(f"Erro durante o processamento: {str(e)}")
            st.error("Detalhes do erro para debug:")
            import traceback
            st.error(traceback.format_exc())

    # Exibe os dados processados diretamente se já estiverem no session_state
    if st.session_state.resultado_final is not None:
        exibir_resumo_pagamentos(st.session_state.resultado_final)

        # Botão de download para o resultado já processado
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'relatorio_marketup_{timestamp}.xlsx'
        save_to_excel(st.session_state.resultado_final, output_path)
        
        with open(output_path, 'rb') as f:
            excel_data = f.read()
        
        st.download_button(
            label="Download Relatório Completo",
            data=excel_data,
            file_name=output_path,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Remover arquivo temporário
        import os
        os.remove(output_path)

    if st.button("Voltar"):
        st.session_state.page = "home"

def exibir_resumo_pagamentos(resultado_final):
    """Função para exibir o resumo de pagamentos."""
    st.markdown('<div class="subtitle">Resumo de Pagamentos</div>', 
               unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        total_cnpjs = len(resultado_final['CNPJ'].unique())
        cnpjs_pagos = len(resultado_final[
            (resultado_final['STATUS_PAGAMENTO'].isin(['PAGO', 'PAGO PARCIALMENTE']))
        ]['CNPJ'].unique())
        
        st.metric("Total de CNPJs", f"{total_cnpjs:,}")
        st.metric("CNPJs Pagos", f"{cnpjs_pagos:,}")
    
    with col2:
        total_mensalidade = resultado_final['VALOR_MENSALIDADE'].apply(
            lambda x: float(x.replace('.', '').replace(',', '.')) if isinstance(x, str) else x
        ).sum()
        
        total_cobrado = resultado_final['VALOR_COBRADO'].apply(
            lambda x: float(x.replace('.', '').replace(',', '.')) if isinstance(x, str) else x
        ).sum()
        
        st.metric("Valor Total Mensalidade", 
                 f"R$ {locale.format_string('%.2f', total_mensalidade, grouping=True)}")
        st.metric("Valor Total Cobrado", 
                 f"R$ {locale.format_string('%.2f', total_cobrado, grouping=True)}")


def menu_extratos_bancarios():
    st.markdown('<div class="title">Processamento de Extratos Bancários</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Arquivo de Entrada</div>', unsafe_allow_html=True)

    # Permite upload de um ou mais arquivos
    uploaded_files = st.file_uploader("Selecione o extrato bancário (Excel)", 
                                      type=['xls', 'xlsx'], 
                                      accept_multiple_files=True) # Ajustar para caso precise processar mais de um arquivo

    if st.button("Processar Arquivo"):
        if not uploaded_files:
            st.error("Por favor, faça upload de apenas um extrato bancário.")
        else:
            try:
                # Chama a função lá do seu script
                df_resultado = processar_extratos(uploaded_files) # Se for processar apenas 1 arquivo por vez, colocar o upload_files entre colchetes
                total_geral = df_resultado['Credito'].sum()

                st.success("Extrato processado com sucesso!")

                # Exibindo os resultados na tela
                st.markdown('<div class="subtitle">Resumo por Instituição</div>', unsafe_allow_html=True)
                # 1. Atualiza o Total usando a sua função format_currency
                st.metric("Valor Total Processado", f"R$ {format_currency(total_geral)}")

                # 2. Atualiza a tabela aplicando a sua função em cada linha da coluna 'Credito'
                st.dataframe(
                    df_resultado.style.format({
                        'Credito': lambda x: f"R$ {format_currency(x)}"
                    }), 
                    use_container_width=True)

                # Criando o buffer para o download do Excel gerado
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_resultado.to_excel(writer, index=False, sheet_name='Resumo_Extratos')
                buffer.seek(0)

                st.download_button(
                    label="Baixar Resultado em Excel",
                    data=buffer,
                    file_name=f"resumo_extratos_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar os arquivos: {e}")

    if st.button("Voltar"):
        st.session_state.page = "home"


def menu_relatorio_financeiro():
    st.markdown('<div class="title">Relatório Financeiro</div>', unsafe_allow_html=True)
    st.write("Conteúdo do Relatório Financeiro.")
    if st.button("Voltar"):
        st.session_state.page = "home"

# Navegação entre as páginas
if st.session_state.page == "home":
    home()
elif st.session_state.page == "menu_tipo_relatorio":
    menu_tipo_relatorio()
elif st.session_state.page == "ap004":
    criacao_agenda()
elif st.session_state.page == "ap007a_ap007b":
    menu_relatorio_cerc()
# elif st.session_state.page == "menu_relatorio_cerc":
#     menu_relatorio_cerc()
elif st.session_state.page == "criacao_contratos":
    criacao_contratos()
elif st.session_state.page == "atualizacao_contratos":
    atualizacao_contratos()
elif st.session_state.page == "inativacao_contratos":
    inativacao_contratos()
elif st.session_state.page == "menu_relatorio_marketup":
    menu_relatorio_marketup()
elif st.session_state.page == "menu_relatorio_financeiro":
    menu_relatorio_financeiro()
elif st.session_state.page == "menu_extratos_bancarios":
    menu_extratos_bancarios()