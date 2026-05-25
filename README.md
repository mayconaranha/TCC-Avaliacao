# TCC — Fatores determinantes da insatisfação do consumidor no e-commerce

**Aluno:** Maycon Henrique Aranha Da Silva
**Orientador:** Gustavo Dantas Lobo
**Curso:** MBA em Data Science e Analytics — USP/Esalq

---

## Sobre o estudo

Este trabalho investiga quais fatores operacionais estão associados à insatisfação do consumidor no e-commerce brasileiro. A insatisfação é medida pela contagem de reviews com notas 1 e 2 que cada vendedor acumula. Como a variável é uma contagem com sobredispersão severa, o modelo de Poisson não serve — o trabalho usa regressão Binomial Negativa NB2 com offset de exposição.

A base é o Brazilian E-Commerce Public Dataset disponibilizado pela Olist no Kaggle, com aproximadamente 100 mil pedidos entre 2016 e 2018. Após o filtro de mínimo 5 reviews por vendedor, a amostra final ficou com 1.754 lojistas.

## Principais resultados

- **Atraso na entrega é o fator mais relevante**: cada dia adicional aumenta em 4,45% a taxa esperada de reviews negativos (p ≈ 10⁻²⁶).
- **Frete tem efeito menor mas significativo**: +0,56% por real (p ≈ 10⁻⁹).
- **Quatro categorias concentram mais reclamações** em relação ao grupo de referência: telefonia (+38,2%), cama/mesa/banho (+33,4%), móveis/decoração (+29,2%) e informática/acessórios (+20,8%).
- **Ticket médio, peso do produto e estado do vendedor** não apresentaram associação significativa após o controle das demais variáveis.
- **Distribuição altamente concentrada** (curva de Lorenz, Gini = 0,747): 20% dos vendedores respondem por 77,9% dos reviews negativos.
- **Simulação contrafactual**: reduzir o atraso médio em 3 dias levaria a uma queda estimada de 12% no total de reviews negativos previstos pelo modelo.

## Método

O fluxo segue Cameron e Trivedi (2013) e Fávero e Belfiore (2024):

1. Poisson como baseline com offset log(total de reviews)
2. Teste de sobredispersão de Cameron-Trivedi (razão variância/média = 52,90; p = 2,31 × 10⁻¹⁵)
3. Estimação do NB2 com α por máxima verossimilhança
4. Seleção de modelo reduzido por AIC, BIC e Pearson χ²/gl
5. Teste de Vuong (NB2 vs ZINB) para checar inflação de zeros — NB2 mantido
6. Análises complementares: curva de Lorenz, efeitos marginais médios, calibração por decis e simulação contrafactual

Ajuste do modelo final: AIC = 6.976,7; Pearson χ²/gl = 1,05.

## Como executar

### 1. Baixar o dataset

A base não está no repositório por ser pública. Faça o download no Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Descompacte os CSVs em `data/`:

```
data/
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
└── product_category_name_translation.csv
```

### 2. Instalar dependências

```bash
pip install pandas numpy statsmodels scipy matplotlib seaborn jupyter statstests python-docx
```

### 3. Rodar os notebooks na ordem

```bash
jupyter notebook
```

| Notebook | O que faz |
|---|---|
| `01_preparacao.ipynb` | Integra as 7 tabelas e agrega por vendedor — gera `data/dataset_vendedores.csv` |
| `02_eda.ipynb` | Distribuições, correlações, VIF e verificação preliminar de sobredispersão |
| `03_modelagem.ipynb` | Poisson, Cameron-Trivedi, NB2 reduzido e teste de Vuong |
| `04_interpretacao.ipynb` | Interpretação por exp(β), tabela comparativa, resíduos de Pearson |

O `01_preparacao.ipynb` precisa rodar antes dos demais — os outros dependem do arquivo `data/dataset_vendedores.csv`.

## Estrutura

```
notebooks/        # análise em Python (preparação, EDA, modelagem, interpretação)
data/             # CSVs da Olist (não versionado, baixar do Kaggle)
outputs/          # figuras e métricas gerados pelos notebooks
[Projeto de pesquisa] - Maycon Henrique Aranha Da Silva.docx
[Resultados Preliminares] - Maycon Henrique Aranha Da Silva.docx
```

## Stack

Python · pandas · numpy · statsmodels · scipy · matplotlib · seaborn · statstests · python-docx
