# Determinantes da insatisfação do consumidor em e-commerce: regressão binomial negativa aplicada a dados transacionais

**Trabalho de Conclusão de Curso** — MBA em Data Science e Analytics (USP/ESALQ)

**Aluno:** Maycon Henrique Aranha da Silva
**Orientador:** Gustavo Dantas Lobo

## Introdução

A satisfação do consumidor é um fator crítico para a sustentabilidade de operações de e-commerce. Avaliações negativas impactam a reputação do vendedor, a taxa de conversão e a retenção de clientes. Compreender quais fatores operacionais e logísticos influenciam a quantidade de avaliações negativas recebidas por um vendedor tem valor prático para a gestão de marketplaces e para a melhoria de processos logísticos.

A variável resposta — número de reviews negativos por vendedor — é uma variável de contagem (valores inteiros não negativos). Quando a variância observada é superior à média, ocorre sobredispersão, o que compromete a adequação do modelo de Poisson. A Regressão Binomial Negativa incorpora um parâmetro adicional de dispersão que acomoda essa variabilidade extra.

## Objetivo

Identificar e quantificar os fatores operacionais e logísticos que influenciam a quantidade de avaliações negativas recebidas por vendedores em uma plataforma de e-commerce, por meio de Regressão Binomial Negativa aplicada a dados transacionais da plataforma Olist.

### Objetivos específicos

1. Construir um dataset agregado por vendedor a partir das bases transacionais do Olist
2. Realizar análise exploratória da distribuição de avaliações negativas
3. Verificar a presença de sobredispersão na variável resposta por meio do teste de Cameron-Trivedi
4. Estimar modelos de Regressão de Poisson e Binomial Negativa com offset de exposição
5. Comparar os modelos por critérios de informação (AIC/BIC) e teste de razão de verossimilhança
6. Interpretar os coeficientes e quantificar o efeito de cada fator sobre a insatisfação

## Dados

Base pública **Olist** (Brazilian E-Commerce Public Dataset), disponível no Kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Tabelas utilizadas:
- `olist_orders_dataset.csv` — pedidos (datas de entrega)
- `olist_order_items_dataset.csv` — itens por pedido (frete, vínculo vendedor-pedido)
- `olist_order_payments_dataset.csv` — pagamentos (valor do pedido)
- `olist_order_reviews_dataset.csv` — avaliações (score 1 a 5)
- `olist_products_dataset.csv` — produtos (peso, categoria)
- `olist_sellers_dataset.csv` — vendedores (estado)
- `product_category_name_translation.csv` — tradução de categorias

## Metodologia

### Unidade de análise

Cada observação é um **vendedor**. As variáveis são agregadas a partir dos pedidos, com filtro para vendedores com pelo menos 5 avaliações recebidas.

### Variável resposta

Número de reviews negativos (score 1 ou 2) por vendedor — variável de contagem com sobredispersão (Var/Média ≈ 52.9).

### Offset (exposição)

O logaritmo do número total de reviews (`log(n_reviews)`) é usado como offset, controlando pela exposição de cada vendedor. Assim o modelo estima a **taxa** de reviews negativos, não a contagem absoluta.

### Variáveis explicativas candidatas

| Variável | Fonte | Tipo |
|---|---|---|
| Atraso médio de entrega (dias) | orders | Contínua |
| Ticket médio (R$) | payments | Contínua |
| Frete médio (R$) | items | Contínua |
| Peso médio dos produtos (g) | products | Contínua |
| Categoria principal do vendedor | products | Categórica |
| Estado do vendedor | sellers | Categórica |

### Modelos

1. Regressão de Poisson (modelo base)
2. Regressão Binomial Negativa (modelo principal)

Ambos estimados por máxima verossimilhança via IRLS, com offset de exposição e interpretação dos coeficientes via exp(b).

### Teste de sobredispersão

Teste de Cameron-Trivedi (regressão auxiliar) e razão Pearson chi²/df.

### Métricas de comparação

- AIC e BIC
- Log-verossimilhança
- Teste de razão de verossimilhança (LR test)
- Pearson chi²/df (adequação do ajuste)

## Estrutura do projeto

```
tcc-insatisfacao-ecommerce/
├── data/                          # Dados brutos (não versionados)
├── notebooks/                     # Notebooks Jupyter (pipeline completo)
│   ├── 01_preparacao.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_modelagem.ipynb
│   └── 04_interpretacao.ipynb
├── outputs/                       # Gráficos, tabelas e resultados
├── tcc-manuais/                   # Templates e manuais USP/ESALQ
├── DESCOBERTAS.md                 # Notas para redação
├── requirements.txt               # Dependências Python
└── README.md
```

## Como executar

```bash
pip install -r requirements.txt
```

Os notebooks devem ser executados em ordem a partir da pasta `notebooks/`:

```
01_preparacao.ipynb   → Carrega as bases, agrega por vendedor, gera dataset
02_eda.ipynb          → Análise exploratória e verificação de sobredispersão
03_modelagem.ipynb    → Estimação Poisson vs BN + testes de sobredispersão
04_interpretacao.ipynb → Interpretação via exp(b), diagnóstico e visualizações
```

## Referências

- Cameron, A.C.; Trivedi, P.K. 2013. *Regression Analysis of Count Data*. Cambridge University Press.
- Fávero, L.P.; Belfiore, P. 2017. *Manual de Análise de Dados*. Elsevier.
- Fávero, L.P.L.; Duarte, A.; Santos, H.P. 2024. A new computational algorithm for assessing overdispersion and zero-inflation in machine learning count models with Python. *Computers* 13(4): 88.
- Hilbe, J.M. 2011. *Negative Binomial Regression*. Cambridge University Press.
