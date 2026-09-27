"""
SalesInsight PY -- Analise de Dados de Vendas
Mini-Projeto Avaliativo - Modulo 1 - Semana 08
Desenvolvedor(a) em IA para Analise Preditiva [T4]

Escopo: apenas biblioteca padrao do Python (csv, json, re, datetime, os, random),
conforme o aviso de escopo reduzido (conteudos ate a Semana 05).
"""

import csv
import json
import os
import random
import re
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# RF01 - Criar ou Carregar o Dataset de Vendas
# ---------------------------------------------------------------------------
def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos e grava em CSV."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = ["id_venda", "data_venda", "cliente", "produto",
               "categoria", "regiao", "quantidade", "preco_unitario"]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            # --- sujeira proposital para a etapa de limpeza ---
            if random.random() < 0.05:
                quantidade = ""                          # valor ausente
            if random.random() < 0.04:
                preco = ""                                # valor ausente
            if random.random() < 0.06:
                produto = " " + produto + " "             # espacos extras
            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"                # data invalida
            if random.random() < 0.10:
                cliente = random.choice([                 # ruido no nome
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#"),
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            })

    print(f"Dataset gerado com {n_registros} registros em {caminho_csv}.")


def carregar_dataset(caminho_csv):
    """Le o CSV e retorna uma lista de dicionarios (um por registro)."""
    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        registros = list(leitor)
    return registros


# ---------------------------------------------------------------------------
# RF02 - Inspecionar e Descrever os Dados
# ---------------------------------------------------------------------------
def inspecionar_dados(registros):
    """Exibe as informacoes estruturais da lista de registros."""
    total = len(registros)
    colunas = list(registros[0].keys()) if registros else []

    nulos = {coluna: 0 for coluna in colunas}
    for linha in registros:
        for coluna in colunas:
            if linha.get(coluna, "").strip() == "":
                nulos[coluna] += 1

    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Total de registros: {total}")
    print(f"\nColunas: {colunas}")
    print(f"\nValores ausentes por coluna:\n{nulos}")
    print("\nPrimeiros registros:")
    for linha in registros[:5]:
        print(linha)
    return registros


# ---------------------------------------------------------------------------
# RF03 - Limpar e Tratar os Dados (datetime e regex)
# ---------------------------------------------------------------------------
def limpar_dados(registros):
    """
    Limpa e trata a lista de registros de vendas.
    Retorna: (registros_limpos, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, removidos e finais.
    """
    relatorio = {"iniciais": len(registros), "removidos_data": 0,
                 "removidos_nulos": 0, "finais": 0}
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    limpos = []

    for linha in registros:
        # 1. remover espacos extras nas colunas de texto
        for chave in ("cliente", "produto", "categoria", "regiao"):
            linha[chave] = linha[chave].strip()

        # 2. converter data_venda e descartar datas invalidas
        try:
            linha["data_venda"] = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        # 3. descartar nulos em quantidade e preco_unitario
        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

        # 4. ajustar os tipos numericos
        linha["quantidade"] = int(float(linha["quantidade"]))
        linha["preco_unitario"] = float(linha["preco_unitario"])

        # 5. padronizar o nome do cliente com re.sub()
        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])
        linha["cliente"] = nome_limpo
        linha["cliente_fora_do_padrao"] = padrao_cliente.match(nome_limpo) is None

        limpos.append(linha)

    # 6. montar e imprimir o relatorio de limpeza
    relatorio["finais"] = len(limpos)
    print("\n=== RELATORIO DE LIMPEZA ===")
    print(relatorio)
    return limpos, relatorio


# ---------------------------------------------------------------------------
# RF04 - Criar Colunas Derivadas com Transformacoes Condicionais
# ---------------------------------------------------------------------------
MESES_PT = {1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}


def criar_colunas_derivadas(registros):
    """Cria receita_total, mes, mes_nome, trimestre, ano e faixa_receita_item."""
    for linha in registros:
        data_venda = linha["data_venda"]
        receita_total = round(linha["quantidade"] * linha["preco_unitario"], 2)

        mes = data_venda.month
        mes_nome = MESES_PT[mes]
        ano = data_venda.year

        if mes <= 3:
            trimestre = "Q1"
        elif mes <= 6:
            trimestre = "Q2"
        elif mes <= 9:
            trimestre = "Q3"
        else:
            trimestre = "Q4"

        if receita_total < 500:
            faixa_receita_item = "Baixo Valor"
        elif receita_total < 5000:
            faixa_receita_item = "Medio Valor"
        else:
            faixa_receita_item = "Alto Valor"

        linha["receita_total"] = receita_total
        linha["mes"] = mes
        linha["mes_nome"] = mes_nome
        linha["trimestre"] = trimestre
        linha["ano"] = ano
        linha["faixa_receita_item"] = faixa_receita_item

    return registros


# ---------------------------------------------------------------------------
# RF05 - Calcular Metricas Agregadas por Mes, Produto, Categoria e Regiao
# ---------------------------------------------------------------------------
def chave_receita(item):
    """Funcao auxiliar usada como criterio de ordenacao (do maior pro menor)."""
    return item["receita_total"]


def calcular_metricas(registros):
    """
    Calcula as metricas agregadas da lista de registros.
    Retorna um dicionario no formato {nome_da_metrica: lista_de_linhas}.
    Chaves: por_mes, top_produtos, por_categoria, por_regiao.
    """
    acumulado_mes = {}
    acumulado_produto = {}
    acumulado_categoria = {}
    acumulado_regiao = {}

    for linha in registros:
        mes = linha["mes"]
        produto = linha["produto"]
        categoria = linha["categoria"]
        regiao = linha["regiao"]
        receita = linha["receita_total"]
        quantidade = linha["quantidade"]

        if mes not in acumulado_mes:
            acumulado_mes[mes] = {"receita_total": 0.0, "quantidade": 0, "n_vendas": 0}
        acumulado_mes[mes]["receita_total"] += receita
        acumulado_mes[mes]["quantidade"] += quantidade
        acumulado_mes[mes]["n_vendas"] += 1

        acumulado_produto[produto] = acumulado_produto.get(produto, 0.0) + receita
        acumulado_categoria[categoria] = acumulado_categoria.get(categoria, 0.0) + receita

        if regiao not in acumulado_regiao:
            acumulado_regiao[regiao] = {"receita_total": 0.0, "n_vendas": 0}
        acumulado_regiao[regiao]["receita_total"] += receita
        acumulado_regiao[regiao]["n_vendas"] += 1

    # monta a lista "por mes" em ordem cronologica
    por_mes = []
    for mes in sorted(acumulado_mes.keys()):
        v = acumulado_mes[mes]
        por_mes.append({
            "mes": mes,
            "receita_total": round(v["receita_total"], 2),
            "quantidade": v["quantidade"],
            "n_vendas": v["n_vendas"],
        })

    # monta a lista de produtos e ordena do maior pro menor faturamento
    lista_produtos = []
    for produto, receita in acumulado_produto.items():
        lista_produtos.append({"produto": produto, "receita_total": round(receita, 2)})
    lista_produtos.sort(key=chave_receita, reverse=True)
    top_produtos = lista_produtos[:5]

    # monta a lista por categoria, tambem ordenada
    por_categoria = []
    for categoria, receita in acumulado_categoria.items():
        por_categoria.append({"categoria": categoria, "receita_total": round(receita, 2)})
    por_categoria.sort(key=chave_receita, reverse=True)

    # monta a lista por regiao, com o ticket medio (receita / numero de vendas)
    por_regiao = []
    for regiao, v in acumulado_regiao.items():
        ticket_medio = v["receita_total"] / v["n_vendas"]
        por_regiao.append({
            "regiao": regiao,
            "receita_total": round(v["receita_total"], 2),
            "ticket_medio": round(ticket_medio, 2),
        })
    por_regiao.sort(key=chave_receita, reverse=True)

    metricas = {
        "por_mes": por_mes,
        "top_produtos": top_produtos,
        "por_categoria": por_categoria,
        "por_regiao": por_regiao,
    }

    print("\n=== POR MES ===")
    for linha in metricas["por_mes"]:
        print(linha)
    print("\n=== TOP PRODUTOS ===")
    for linha in metricas["top_produtos"]:
        print(linha)
    print("\n=== POR CATEGORIA ===")
    for linha in metricas["por_categoria"]:
        print(linha)
    print("\n=== POR REGIAO (receita e ticket medio) ===")
    for linha in metricas["por_regiao"]:
        print(linha)

    return metricas


# ---------------------------------------------------------------------------
# RF06 - Segmentar Clientes por Nivel de Gasto
# ---------------------------------------------------------------------------
def chave_gasto(cliente):
    """Funcao auxiliar usada como criterio de ordenacao dos clientes."""
    return cliente["total_gasto"]


def segmentar_clientes(registros):
    """
    Agrupa por cliente, soma a receita e classifica em Bronze/Prata/Ouro
    usando uma funcao lambda.
    Retorna uma lista de dicionarios: cliente, total_gasto, segmento.
    """
    classificar = lambda total: (
        "Ouro" if total > 15000 else "Prata" if total >= 5000 else "Bronze"
    )

    total_por_cliente = {}
    for linha in registros:
        total_por_cliente[linha["cliente"]] = (
            total_por_cliente.get(linha["cliente"], 0.0) + linha["receita_total"]
        )

    # aplica a lambda "classificar" dentro de um laco, para cada cliente
    clientes = []
    for nome, total in total_por_cliente.items():
        clientes.append({
            "cliente": nome,
            "total_gasto": round(total, 2),
            "segmento": classificar(total),
        })
    clientes.sort(key=chave_gasto, reverse=True)

    distribuicao = {"Bronze": 0, "Prata": 0, "Ouro": 0}
    for c in clientes:
        distribuicao[c["segmento"]] += 1

    print("\n=== TOP 10 CLIENTES ===")
    for c in clientes[:10]:
        print(c)
    print("\n=== DISTRIBUICAO DE CLIENTES POR SEGMENTO ===")
    print(distribuicao)

    return clientes


# ---------------------------------------------------------------------------
# RF07 - Organizar o Codigo em Funcoes Reutilizaveis (funcao de ordem superior)
# ---------------------------------------------------------------------------
def processar_coluna(registros, coluna, funcao_transformacao, nome_saida=None):
    """
    Aplica uma funcao de transformacao a um campo de cada registro.
    Demonstra o uso de funcoes como argumento (funcao de ordem superior).
    """
    nome_saida = nome_saida or f"{coluna}_transformado"
    for linha in registros:
        linha[nome_saida] = funcao_transformacao(linha[coluna])
    return registros


# ---------------------------------------------------------------------------
# Estatisticas gerais (RF08 - insumo para o JSON exportado)
# ---------------------------------------------------------------------------
def calcular_estatisticas_gerais(registros):
    """Calcula estatisticas gerais do dataset limpo, incluindo vendas acima da media."""
    total_registros = len(registros)
    receita_total_geral = 0.0
    for linha in registros:
        receita_total_geral += linha["receita_total"]
    media_receita_por_venda = receita_total_geral / total_registros if total_registros else 0

    vendas_acima_da_media = 0
    for linha in registros:
        if linha["receita_total"] > media_receita_por_venda:
            vendas_acima_da_media += 1

    estatisticas = {
        "total_registros": total_registros,
        "receita_total_geral": round(receita_total_geral, 2),
        "media_receita_por_venda": round(media_receita_por_venda, 2),
        "vendas_acima_da_media": vendas_acima_da_media,
    }

    print("\n=== ESTATISTICAS GERAIS ===")
    print(estatisticas)
    return estatisticas


# ---------------------------------------------------------------------------
# RF08 - Exportar Resultados em CSV e JSON
# ---------------------------------------------------------------------------
def exportar_resultados(metricas, clientes, estatisticas):
    """Exporta os resultados do projeto em CSV e JSON."""
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/metricas_por_mes.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=metricas["por_mes"][0].keys())
        escritor.writeheader()
        escritor.writerows(metricas["por_mes"])

    with open("outputs/segmentacao_clientes.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=clientes[0].keys())
        escritor.writeheader()
        escritor.writerows(clientes)

    caminho = "outputs/estatisticas_gerais.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(estatisticas, f, indent=4, ensure_ascii=False)

    # leitura de volta para confirmar a escrita
    with open(caminho, "r", encoding="utf-8") as f:
        conferencia = json.load(f)
    print(f"\nJSON gravado e lido: {conferencia}")


# ---------------------------------------------------------------------------
# RF09 - Executar o Fluxo Completo (Ponto de Entrada)
# ---------------------------------------------------------------------------
def main():
    """Executa o fluxo completo do SalesInsight PY."""
    print("=" * 60)
    print(" SALESINSIGHT PY - Analise de Dados de Vendas")
    print("=" * 60)

    # Etapa 0 - garantir a existencia do dataset
    if not os.path.exists("vendas.csv"):
        gerar_dataset_vendas("vendas.csv")

    # Etapas 1 a 8 - fluxo pelas funcoes (limpeza sempre antes das agregacoes)
    registros = carregar_dataset("vendas.csv")
    inspecionar_dados(registros)
    registros_limpos, relatorio_limpeza = limpar_dados(registros)
    registros_limpos = criar_colunas_derivadas(registros_limpos)

    # demonstracao da funcao de ordem superior com lambdas em contextos distintos
    registros_limpos = processar_coluna(
        registros_limpos, "receita_total",
        lambda x: round(x / 1000, 2),
        nome_saida="receita_em_milhares",
    )
    registros_limpos = processar_coluna(
        registros_limpos, "quantidade",
        lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
        nome_saida="perfil_volume",
    )

    metricas = calcular_metricas(registros_limpos)
    clientes = segmentar_clientes(registros_limpos)
    estatisticas = calcular_estatisticas_gerais(registros_limpos)
    exportar_resultados(metricas, clientes, estatisticas)

    print("\n[CONCLUIDO] Fluxo finalizado com sucesso.")


if __name__ == "__main__":
    main()
