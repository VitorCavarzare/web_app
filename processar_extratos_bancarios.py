import pandas as pd

def processar_extratos(arquivos_upload):
    headers = ['Data', 'Lancamento', 'Dcto', 'Credito', 'Debito', 'Saldo']
    
    credenciadoras = [
        "CIELO S.A - INSTITUICAO DE PAGAMENTO",
        "BANCO COOPERATIVO SICREDI S.A.",
        "REDECARD INSTITUICAO DE PAGAMENTO S.A.",
        "QUERO-QUERO VERDECARD INSTITUICAO DE PAGAMENTO S.A",
        "BANCO COOPERATIVO SICOOB S.A.",
        "SEM PARAR INSTITUICAO DE PAGAMENTO LTDA",
        "FISERV DO BRASIL INSTITUICAO DE PAGAMENTO LTDA",
        "PUNTO INSTITUICAO DE PAGAMENTO HOZ LTDA.",
        "PAYGO ADMINISTRADORA DE MEIOS DE PAGAMENTOS LTDA",
        "PAGSEGURO INTERNET INSTITUICAO DE PAGAMENTO S.A.",
        "DOCK SOLUCOES INSTITUICAO DE PAGAMENTO SA",
        "EFI S.A. - INSTITUICAO DE PAGAMENTO",
        "GRUPOCARD COMERCIO DE CARTOES TELEFONICOS LTDA",
        "GETNET ADQUIRENCIA E SERVICOS PARA MEIOS DE PAGAMENTO S.A. - INSTITUICAO DE PAGAMENTO",
        "MERCADO PAGO INSTITUICAO DE PAGAMENTO LTDA",
        "HUB INSTITUICAO DE PAGAMENTO S.A.",
        "YAPAY PAGAMENTOS ONLINE S/A",
        "IFOOD.COM AGENCIA DE RESTAURANTES ONLINE S.A.",
        "STELO S.A.",
        "ADYEN DO BRASIL INSTITUICAO DE PAGAMENTO LTDA.",
        "AMAZON SERVICOS DE VAREJO DO BRASIL LTDA.",
        "STONE INSTITUICAO DE PAGAMENTO S.A",
        "SUMUP INSTITUICAO DE PAGAMENTO BRASIL LTDA",
        "PINBANK BRASIL INSTITUICAO DE PAGAMENTO S.A.",
        "BANCO TRIANGULO S/A",
        "ENTREPAY INSTITUICAO DE PAGAMENTO S.A",
        "CLOUDWALK INSTITUICAO DE PAGAMENTO E SERVICOS LTDA",
        "PAGAR.ME INSTITUICAO DE PAGAMENTO S.A",
        "ADIQPLUS INSTITUICAO DE PAGAMENTO LTDA",
        "ZOOP TECNOLOGIA & INSTITUICAO DE PAGAMENTO S.A.",
        "ASAAS GESTAO FINANCEIRA INSTITUICAO DE PAGAMENTO S.A.",
        "STRIPE BRASIL SOLUCOES DE PAGAMENTO INSTITUICAO DE PAGAMENTO LTDA",
        "GRANITO INSTITUICAO DE PAGAMENTO S.A.",
        "PICPAY INSTITUICAO DE PAGAMENTO S/A",
        "AMO SISTEMAS LTDA",
        "AMERICA PAYMENT S.A.",
        "EBANX PAGAMENTOS LTDA",
        "RAPPI BRASIL INTERMEDIACAO DE NEGOCIOS LTDA",
        "APPMAX PLATAFORMA DE PAGAMENTOS LTDA",
        "MAISTODOS S.A.",
        "SAFE2PAY INSTITUICAO DE PAGAMENTO LTDA",
        "SQUID MEIOS DE PAGAMENTOS LTDA",
        "VALORI LTDA",
        "VERSA S.A.",
        "BEE2PAY TRAVEL SOLUTIONS S.A",
        "PAYTIME FINTECH LTDA",
        "TUNA PAGAMENTOS LTDA",
        "MEEP PAGAMENTOS S.A.",
        "BANCO SAFRA S A",
        "99 FOOD LTDA",
        "BANRISUL SOLUCOES EM PAGAMENTOS S.A. - INSTITUICAO DE PAGAMENTO"
    ]

    def extrair_keyword(nome):
        partes = nome.upper().replace('.', '').replace('-', '').split()
        if partes[0] in ['BANCO', 'REDE', 'VERO']:
            return partes[1]
        return partes[0]

    mapa_keywords = {extrair_keyword(inst): inst for inst in credenciadoras}
    keywords = list(mapa_keywords.keys())

    def identificar_instituicao(texto):
        texto_upper = str(texto).upper()
        for kw in keywords:
            if kw in texto_upper:
                return mapa_keywords[kw]
        return "Outros / Não Identificado"

    lista_dfs = []

    # Processa cada arquivo recebido
    for arquivo in arquivos_upload:
        df = pd.read_excel(arquivo, skiprows=10, header=None, names=headers)

        indice_total = df[df.iloc[:, 0] == 'Total'].index[0]
        df_limpo = df.iloc[:indice_total].copy()

        df_limpo['Credito'] = (df_limpo['Credito']
                               .astype(str)
                               .str.replace('.', '', regex=False)
                               .str.replace(',', '.', regex=False)
                               .astype(float))

        df_limpo['Instituicao'] = df_limpo['Lancamento'].apply(identificar_instituicao)
        df_final = df_limpo[df_limpo['Instituicao'] != "Outros / Não Identificado"].copy()
        
        lista_dfs.append(df_final)

    # Concatena todos os dados de todos os arquivos
    df_consolidado = pd.concat(lista_dfs, ignore_index=True)

    # Agrupa por Instituição e soma os valores
    df_agrupado = df_consolidado.groupby('Instituicao')['Credito'].sum().reset_index()
    df_agrupado = df_agrupado.sort_values(by='Credito', ascending=False)

    return df_agrupado