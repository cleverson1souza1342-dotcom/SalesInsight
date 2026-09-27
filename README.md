# SalesInsight PY

## Sobre o projeto

O **SalesInsight PY** é um mini-projeto de análise de dados de vendas desenvolvido em Python.

O projeto trabalha com um conjunto de dados de vendas contendo informações como cliente, produto, categoria, região, quantidade e preço unitário. O programa realiza todo o fluxo de preparação e análise dos dados: criação/carregamento do dataset, inspeção, limpeza, transformação, cálculo de métricas, segmentação de clientes e exportação dos resultados.

O projeto utiliza apenas bibliotecas padrão do Python.

## Bibliotecas utilizadas

- `csv` — leitura e gravação de arquivos CSV
- `json` — criação e leitura de arquivos JSON
- `os` — manipulação de caminhos, pastas e verificação de arquivos
- `random` — geração dos dados sintéticos
- `re` — expressões regulares utilizadas na limpeza dos nomes dos clientes
- `datetime` e `timedelta` — criação, validação e manipulação das datas

## Estrutura do projeto

```text
SalesInsight/
├── salesinsight.py
├── vendas.csv
├── README.md
└── outputs/
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    └── estatisticas_gerais.json
```

> Caso `vendas.csv` ainda não exista, o próprio programa gera o dataset automaticamente. A pasta `outputs` também é criada durante a execução.

## Requisitos funcionais

### RF01 — Criar ou carregar o dataset de vendas

O programa verifica a existência do arquivo `vendas.csv`. Caso ele não exista, é criado um dataset sintético com registros de vendas.

O dataset contém dados como:

- ID da venda
- Data da venda
- Cliente
- Produto
- Categoria
- Região
- Quantidade
- Preço unitário

Também são inseridas propositalmente algumas inconsistências, como valores ausentes, espaços extras, datas inválidas e ruídos nos nomes dos clientes. Esses problemas são utilizados posteriormente para demonstrar a etapa de limpeza.

### RF02 — Inspecionar e descrever os dados

Após carregar o dataset, o programa realiza uma inspeção inicial, apresentando:

- Total de registros
- Colunas existentes
- Quantidade de valores ausentes por coluna
- Primeiros cinco registros

Essa etapa permite conhecer a estrutura e a situação inicial dos dados.

### RF03 — Limpar e tratar os dados

O programa realiza o tratamento dos registros antes das análises.

Entre as operações realizadas estão:

- Remoção de espaços extras
- Validação e conversão das datas
- Remoção de registros com datas inválidas
- Remoção de registros sem quantidade ou preço unitário
- Conversão de quantidade e preço para tipos numéricos
- Padronização dos nomes dos clientes utilizando expressões regulares

Ao final, é apresentado um relatório com a quantidade de registros iniciais, removidos e finais.

### RF04 — Criar colunas derivadas

Com os dados já tratados, são criadas novas informações para auxiliar nas análises.

As principais colunas criadas são:

- `receita_total`
- `mes`
- `mes_nome`
- `trimestre`
- `ano`
- `faixa_receita_item`

A receita total é calculada multiplicando a quantidade vendida pelo preço unitário.

As vendas também são classificadas como **Baixo Valor**, **Médio Valor** ou **Alto Valor**.

### RF05 — Calcular métricas agregadas

O programa calcula métricas de vendas agrupadas por diferentes dimensões.

São geradas análises:

- Por mês
- Por produto
- Por categoria
- Por região

Também são identificados os cinco produtos com maior faturamento e calculado o ticket médio por região.

### RF06 — Segmentar clientes por nível de gasto

Os clientes são agrupados de acordo com o total gasto e classificados em três segmentos:

- **Bronze:** abaixo de R$ 5.000
- **Prata:** de R$ 5.000 até R$ 15.000
- **Ouro:** acima de R$ 15.000

A classificação utiliza uma função `lambda`.

O programa também apresenta os dez clientes com maior gasto e a distribuição de clientes por segmento.

### RF07 — Organizar o código em funções reutilizáveis

O projeto utiliza funções para organizar e reaproveitar o código.

A função `processar_coluna()` demonstra o uso de uma função de ordem superior, recebendo uma função de transformação como argumento.

Ela é utilizada para criar informações como:

- Receita em milhares
- Perfil de volume da venda

### RF08 — Calcular estatísticas e exportar os resultados

O programa calcula estatísticas gerais do dataset tratado:

- Total de registros
- Receita total geral
- Média de receita por venda
- Quantidade de vendas acima da média

Depois, os resultados são exportados para a pasta `outputs`.

Arquivos gerados:

- `metricas_por_mes.csv`
- `segmentacao_clientes.csv`
- `estatisticas_gerais.json`

O arquivo JSON é lido novamente após a gravação para confirmar que a escrita foi realizada corretamente.

### RF09 — Executar o fluxo completo

A função `main()` é o ponto de entrada do programa e executa todas as etapas na ordem correta:

1. Verifica ou gera o dataset
2. Carrega os dados
3. Inspeciona os registros
4. Limpa e trata os dados
5. Cria as colunas derivadas
6. Aplica transformações reutilizáveis
7. Calcula as métricas
8. Segmenta os clientes
9. Calcula as estatísticas gerais
10. Exporta os resultados

Ao final da execução, o programa informa que o fluxo foi concluído com sucesso.

## Como executar

### Requisitos

- Python 3 instalado

Como o projeto utiliza apenas bibliotecas padrão do Python, não é necessário instalar pacotes externos.

### Execução

No terminal, acesse a pasta do projeto e execute:

```bash
python salesinsight.py
```

Em alguns sistemas, o comando pode ser:

```bash
python3 salesinsight.py
```

Se o arquivo `vendas.csv` não existir, ele será criado automaticamente. Após a execução, os resultados serão gravados na pasta `outputs`.

## Fluxo resumido

```text
vendas.csv
    ↓
Carregamento
    ↓
Inspeção
    ↓
Limpeza
    ↓
Criação de novas colunas
    ↓
Cálculo de métricas
    ↓
Segmentação de clientes
    ↓
Estatísticas gerais
    ↓
Exportação CSV / JSON
```

## Objetivo

O objetivo do projeto é aplicar conceitos fundamentais de Python em um fluxo completo de análise de dados, utilizando funções, estruturas condicionais, laços de repetição, manipulação de arquivos CSV e JSON, expressões regulares, datas, funções `lambda` e funções de ordem superior.

## Autor

**Cleverson Souza**

Mini-Projeto Avaliativo — Módulo 1 — Semana 08  
Desenvolvedor(a) em IA para Análise Preditiva [T4]
