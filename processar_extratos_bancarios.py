import pandas as pd

def processar_extratos(arquivos_upload):
    headers = ['Data', 'Lancamento', 'Dcto', 'Credito', 'Debito', 'Saldo']
    
    mapa_busca = {
        "CIELO": "CIELO S.A - INSTITUICAO DE PAGAMENTO",
        "SICREDI": "BANCO COOPERATIVO SICREDI S.A.",
        "REDE": "REDECARD INSTITUICAO DE PAGAMENTO S.A.",
        "REDECARD": "REDECARD INSTITUICAO DE PAGAMENTO S.A.",
        "QUERO-QUERO": "QUERO-QUERO VERDECARD INSTITUICAO DE PAGAMENTO S.A",
        "VERDECARD": "QUERO-QUERO VERDECARD INSTITUICAO DE PAGAMENTO S.A",
        "SICOOB": "BANCO COOPERATIVO SICOOB S.A.",
        "SEM PARAR": "SEM PARAR INSTITUICAO DE PAGAMENTO LTDA",
        "FISERV": "FISERV DO BRASIL INSTITUICAO DE PAGAMENTO LTDA",
        "BIN ": "FISERV DO BRASIL INSTITUICAO DE PAGAMENTO LTDA",
        "PUNTO": "PUNTO INSTITUICAO DE PAGAMENTO HOZ LTDA.",
        "PAYGO": "PAYGO ADMINISTRADORA DE MEIOS DE PAGAMENTOS LTDA",
        "PAGSEGURO": "PAGSEGURO INTERNET INSTITUICAO DE PAGAMENTO S.A.",
        "DOCK": "DOCK SOLUCOES INSTITUICAO DE PAGAMENTO SA",
        "EFI ": "EFI S.A. - INSTITUICAO DE PAGAMENTO",
        "GERENCIANET": "EFI S.A. - INSTITUICAO DE PAGAMENTO",
        "GRUPOCARD": "GRUPOCARD COMERCIO DE CARTOES TELEFONICOS LTDA",
        "GETNET": "GETNET ADQUIRENCIA E SERVICOS PARA MEIOS DE PAGAMENTO S.A. - INSTITUICAO DE PAGAMENTO",
        "MERCADO PAGO": "MERCADO PAGO INSTITUICAO DE PAGAMENTO LTDA",
        "MERCADOPAGO": "MERCADO PAGO INSTITUICAO DE PAGAMENTO LTDA",
        "HUB ": "HUB INSTITUICAO DE PAGAMENTO S.A.",
        "YAPAY": "YAPAY PAGAMENTOS ONLINE S/A",
        "STELO": "STELO S.A.",
        "ADYEN": "ADYEN DO BRASIL INSTITUICAO DE PAGAMENTO LTDA.",
        "AMAZON": "AMAZON SERVICOS DE VAREJO DO BRASIL LTDA.",
        "STONE": "STONE INSTITUICAO DE PAGAMENTO S.A",
        "SUMUP": "SUMUP INSTITUICAO DE PAGAMENTO BRASIL LTDA",
        "PINBANK": "PINBANK BRASIL INSTITUICAO DE PAGAMENTO S.A.",
        "TRIANGULO": "BANCO TRIANGULO S/A",
        "ENTREPAY": "ENTREPAY INSTITUICAO DE PAGAMENTO S.A",
        "CLOUDWALK": "CLOUDWALK INSTITUICAO DE PAGAMENTO E SERVICOS LTDA",
        "INFINITEPAY": "CLOUDWALK INSTITUICAO DE PAGAMENTO E SERVICOS LTDA",
        "ADIQ": "ADIQPLUS INSTITUICAO DE PAGAMENTO LTDA",
        "ZOOP": "ZOOP TECNOLOGIA & INSTITUICAO DE PAGAMENTO S.A.",
        "ASAAS": "ASAAS GESTAO FINANCEIRA INSTITUICAO DE PAGAMENTO S.A.",
        "STRIPE": "STRIPE BRASIL SOLUCOES DE PAGAMENTO INSTITUICAO DE PAGAMENTO LTDA",
        "GRANITO": "GRANITO INSTITUICAO DE PAGAMENTO S.A.",
        "PICPAY": "PICPAY INSTITUICAO DE PAGAMENTO S/A",
        "AMO SISTEMAS": "AMO SISTEMAS LTDA",
        "AMERICA PAYMENT": "AMERICA PAYMENT S.A.",
        "EBANX": "EBANX PAGAMENTOS LTDA",
        "RAPPI": "RAPPI BRASIL INTERMEDIACAO DE NEGOCIOS LTDA",
        "APPMAX": "APPMAX PLATAFORMA DE PAGAMENTOS LTDA",
        "MAISTODOS": "MAISTODOS S.A.",
        "SAFE2PAY": "SAFE2PAY INSTITUICAO DE PAGAMENTO LTDA",
        "SQUID": "SQUID MEIOS DE PAGAMENTOS LTDA",
        "VALORI": "VALORI LTDA",
        "VERSA": "VERSA S.A.",
        "BEE2PAY": "BEE2PAY TRAVEL SOLUTIONS S.A",
        "PAYTIME": "PAYTIME FINTECH LTDA",
        "TUNA": "TUNA PAGAMENTOS LTDA",
        "MEEP": "MEEP PAGAMENTOS S.A.",
        "SAFRA": "BANCO SAFRA S A",
        "BANRISUL": "BANRISUL SOLUCOES EM PAGAMENTOS S.A. - INSTITUICAO DE PAGAMENTO",
        "VERO ": "BANRISUL SOLUCOES EM PAGAMENTOS S.A. - INSTITUICAO DE PAGAMENTO",
        # ---> LINHA ADICIONADA AQUI <---
        "TED-TRANSF ELET DISPON REMET": "TED-TRANSF ELET DISPON REMET."
    }

    def identificar_instituicao(texto):
        if pd.isna(texto): return "Outros / Não Identificado"
        texto_upper = str(texto).upper()
        
        # Prioridade Máxima
        if "IFOOD" in texto_upper:
            return "IFOOD.COM AGENCIA DE RESTAURANTES ONLINE S.A."
        if "99 FOOD" in texto_upper or "99FOOD" in texto_upper:
            return "99 FOOD LTDA"
        if "PAGAR.ME" in texto_upper or "PAGARME" in texto_upper:
            return "PAGAR.ME INSTITUICAO DE PAGAMENTO S.A"

        # Varre o dicionário
        for apelido, nome_oficial in mapa_busca.items():
            if apelido in texto_upper:
                return nome_oficial
                
        return "Outros / Não Identificado"

    def limpar_valor(x):
        if pd.isna(x): return 0.0
        if isinstance(x, (int, float)): return float(x)
        x_str = str(x).strip()
        if x_str in ['', '-']: return 0.0
        if ',' in x_str and '.' in x_str:
            x_str = x_str.replace('.', '').replace(',', '.')
        elif ',' in x_str:
            x_str = x_str.replace(',', '.')
        try:
            return float(x_str)
        except:
            return 0.0

    lista_dfs = []

    for arquivo in arquivos_upload:
        df = pd.read_excel(arquivo, skiprows=10, header=None, names=headers)

        # =========================================================================
        # 1. CORTE DOS LANÇAMENTOS FUTUROS
        # =========================================================================
        # Procura a frase "Lançamentos Futuros" na primeira coluna
        mask_futuros = df['Data'].astype(str).str.contains("Lançamentos Futuros", case=False, na=False)
        
        if mask_futuros.any():
            # Descobre a linha exata onde a palavra apareceu e deleta tudo dali para baixo!
            indice_futuros = df[mask_futuros].index[0]
            df = df.iloc[:indice_futuros].copy()

        # =========================================================================
        # 2. FILTRAGEM SEGURA DE DATAS (Ignora 'Total', linhas vazias, etc.)
        # =========================================================================
        # Tenta extrair e converter apenas datas reais no formato esperado
        df['Data_Str'] = df['Data'].astype(str).str.strip().str.slice(0, 10)
        df['Data_Real'] = pd.to_datetime(df['Data_Str'], format='%d/%m/%Y', errors='coerce')
        df['Data_Real'] = df['Data_Real'].fillna(pd.to_datetime(df['Data_Str'], errors='coerce'))

        # Mantém APENAS linhas que têm data válida na coluna (exclui o lixo)
        df_limpo = df.dropna(subset=['Data_Real']).copy()

        # Aplica a limpeza de valores para evitar números inflacionados
        df_limpo['Credito'] = df_limpo['Credito'].apply(limpar_valor)
        
        # Identifica a instituição
        df_limpo['Instituicao'] = df_limpo['Lancamento'].apply(identificar_instituicao)
        
        # Guarda apenas o que foi identificado e tem valor efetivo > 0
        df_final = df_limpo[(df_limpo['Instituicao'] != "Outros / Não Identificado") & (df_limpo['Credito'] > 0)].copy()
        
        lista_dfs.append(df_final)

    if not lista_dfs:
        return pd.DataFrame()

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)

    # Formata a data para a visualização final e exportação
    df_consolidado['Data_Exibicao'] = df_consolidado['Data_Real'].dt.strftime('%d/%m/%Y')

    # Agrupa e Soma!
    df_agrupado = df_consolidado.groupby(['Data_Real', 'Data_Exibicao', 'Instituicao'])['Credito'].sum().reset_index()

    # Ordena cronologicamente e do maior para o menor valor do dia
    df_agrupado = df_agrupado.sort_values(by=['Data_Real', 'Credito'], ascending=[True, False])

    # Limpa as colunas técnicas antes de devolver à tela
    df_agrupado = df_agrupado.drop(columns=['Data_Real'])
    df_agrupado = df_agrupado.rename(columns={'Data_Exibicao': 'Data'})

    return df_agrupado