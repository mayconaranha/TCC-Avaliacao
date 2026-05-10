# TCC — Fatores operacionais associados à insatisfação expressa em reviews negativos no e-commerce brasileiro

**Aluno:** Maycon Henrique Aranha Da Silva  
**Orientador:** Gustavo Dantas Lobo  
**Curso:** MBA em Data Science e Analytics — USP/Esalq

---

## Sobre o estudo

Investigação dos fatores operacionais que determinam a taxa de insatisfação do consumidor no e-commerce brasileiro, medida pela contagem de reviews negativos (notas 1 e 2) por vendedor.

**Dados:** Brazilian E-Commerce Public Dataset (Olist, 2018) — base pública disponível no Kaggle.  
**Método:** Regressão para dados de contagem (Poisson e Binomial Negativa NB2) com offset de exposição.  
**Amostra:** 1.754 vendedores com no mínimo 5 reviews.

---

## Como executar os notebooks

### 1. Baixar o dataset

O dataset não está incluído no repositório pois é público. Faça o download diretamente no Kaggle:

**Link:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Após o download, descompacte o arquivo e coloque os CSVs na pasta `data/` com a seguinte estrutura:

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

### 2. Instalar as dependências

```bash
pip install pandas numpy statsmodels scipy matplotlib seaborn jupyter statstests
```

### 3. Executar na ordem

```bash
jupyter notebook
```

Execute os notebooks na sequência:

| Notebook | O que faz |
|---|---|
| `01_preparacao.ipynb` | Integra as 7 tabelas e agrega por vendedor — gera `data/dataset_vendedores.csv` |
| `02_eda.ipynb` | Análise exploratória, distribuições, correlações e VIF |
| `03_modelagem.ipynb` | Poisson baseline, Cameron-Trivedi, NB2 MLE, Vuong (NB2 vs ZINB) |
| `04_interpretacao.ipynb` | Coeficientes via exp(β), tabelas e gráficos de diagnóstico |

> **Atenção:** execute sempre o `01_preparacao.ipynb` primeiro — os demais dependem do arquivo `data/dataset_vendedores.csv` que ele gera.

---

## Estrutura do repositório

```
notebooks/
├── 01_preparacao.ipynb      # Integração e agregação dos dados por vendedor
├── 02_eda.ipynb             # Análise exploratória e verificação de VIF
├── 03_modelagem.ipynb       # Poisson, Cameron-Trivedi, NB2 MLE, Vuong test
└── 04_interpretacao.ipynb   # Interpretação via exp(β) e diagnóstico

[Projeto de pesquisa] - Maycon Henrique Aranha Da Silva.docx   # Projeto aprovado
Resultados_Preliminares_Maycon.docx  # Resultados preliminares
```

---

## Tecnologias

Python · pandas · numpy · statsmodels · scipy · matplotlib · seaborn · statstests
 
