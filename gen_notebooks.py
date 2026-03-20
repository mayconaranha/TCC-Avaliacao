"""Gera os 4 notebooks do pipeline."""
import json, os

OUTDIR = "notebooks"

def make_nb(cells_data, filename):
    cells = []
    for ctype, src in cells_data:
        cell = {"cell_type": ctype, "metadata": {}, "source": [src]}
        if ctype == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        cells.append(cell)
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "nbformat": 4, "nbformat_minor": 4
    }
    path = os.path.join(OUTDIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"  {path}")


# =====================================================================
# 01 - PREPARACAO
# =====================================================================
nb01 = [
("markdown", """# 01 — Preparação dos Dados

Construção do dataset agregado por vendedor a partir das bases transacionais do Olist.

**Unidade de análise:** vendedor
**Filtros:** pedidos com status delivered, vendedores com pelo menos 5 reviews"""),

("code", """import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

DATA = "../data/"

orders = pd.read_csv(f"{DATA}olist_orders_dataset.csv",
    parse_dates=["order_purchase_timestamp", "order_delivered_customer_date",
                 "order_estimated_delivery_date"])
items = pd.read_csv(f"{DATA}olist_order_items_dataset.csv")
payments = pd.read_csv(f"{DATA}olist_order_payments_dataset.csv")
reviews = pd.read_csv(f"{DATA}olist_order_reviews_dataset.csv")
products = pd.read_csv(f"{DATA}olist_products_dataset.csv")
sellers = pd.read_csv(f"{DATA}olist_sellers_dataset.csv")
cat_trans = pd.read_csv(f"{DATA}product_category_name_translation.csv")

print(f"Orders:   {len(orders):,}")
print(f"Items:    {len(items):,}")
print(f"Payments: {len(payments):,}")
print(f"Reviews:  {len(reviews):,}")
print(f"Products: {len(products):,}")
print(f"Sellers:  {len(sellers):,}")"""),

("markdown", "## 1. Reviews negativos por pedido"),

("code", """delivered = orders[orders["order_status"] == "delivered"].copy()
print(f"Pedidos entregues: {len(delivered):,}")

rev = reviews[["order_id", "review_score"]].merge(delivered[["order_id"]], on="order_id")
rev["is_negative"] = (rev["review_score"] <= 2).astype(int)
print(f"Reviews de pedidos entregues: {len(rev):,}")
print(f"Reviews negativos (score 1-2): {rev['is_negative'].sum():,} ({rev['is_negative'].mean()*100:.1f}%)")
print(f"\\nDistribuicao review_score:")
print(rev["review_score"].value_counts().sort_index())"""),

("markdown", "## 2. Vínculo pedido-vendedor"),

("code", """order_seller = items[["order_id", "seller_id"]].drop_duplicates("order_id")
rev = rev.merge(order_seller, on="order_id", how="left")
print(f"Reviews com seller_id: {rev['seller_id'].notna().sum():,}")"""),

("markdown", "## 3. Agregação por vendedor — variável resposta"),

("code", """seller_agg = rev.groupby("seller_id").agg(
    n_reviews=("review_score", "count"),
    n_negative=("is_negative", "sum"),
    review_mean=("review_score", "mean")
).reset_index()

print(f"Vendedores com reviews: {len(seller_agg):,}")
print(f"\\nDistribuicao de n_reviews:")
print(seller_agg["n_reviews"].describe())"""),

("markdown", "## 4. Variáveis explicativas por vendedor"),

("code", """# Atraso medio de entrega
delivered["atraso_dias"] = (
    delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
).dt.days
order_atraso = delivered[["order_id", "atraso_dias"]].merge(order_seller, on="order_id")
atraso_seller = order_atraso.groupby("seller_id")["atraso_dias"].mean().reset_index(name="atraso_medio")

# Ticket medio
order_pay = payments.groupby("order_id")["payment_value"].sum().reset_index()
order_pay = order_pay.merge(order_seller, on="order_id")
ticket_seller = order_pay.groupby("seller_id")["payment_value"].mean().reset_index(name="ticket_medio")

# Frete medio
order_frete = items.groupby("order_id")["freight_value"].sum().reset_index()
order_frete = order_frete.merge(order_seller, on="order_id")
frete_seller = order_frete.groupby("seller_id")["freight_value"].mean().reset_index(name="frete_medio")

# Peso medio dos produtos
item_prod = items[["order_id", "seller_id", "product_id"]].merge(
    products[["product_id", "product_weight_g"]], on="product_id")
peso_seller = item_prod.groupby("seller_id")["product_weight_g"].mean().reset_index(name="peso_medio")

# Categoria principal do vendedor
item_cat = items[["seller_id", "product_id"]].merge(
    products[["product_id", "product_category_name"]], on="product_id")
item_cat = item_cat.merge(cat_trans, on="product_category_name", how="left")
cat_principal = item_cat.groupby("seller_id")["product_category_name_english"].agg(
    lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "other"
).reset_index(name="categoria_principal")

# Estado do vendedor
seller_state = sellers[["seller_id", "seller_state"]]

print("Variaveis calculadas: atraso_medio, ticket_medio, frete_medio, peso_medio, categoria_principal, seller_state")"""),

("markdown", "## 5. Junção e filtros"),

("code", """df = seller_agg.merge(atraso_seller, on="seller_id", how="left")
df = df.merge(ticket_seller, on="seller_id", how="left")
df = df.merge(frete_seller, on="seller_id", how="left")
df = df.merge(peso_seller, on="seller_id", how="left")
df = df.merge(cat_principal, on="seller_id", how="left")
df = df.merge(seller_state, on="seller_id", how="left")

print(f"Antes dos filtros: {len(df):,} vendedores")
print(f"NAs por coluna:")
print(df.isnull().sum())

# Filtrar: min 5 reviews + sem NAs
df = df[df["n_reviews"] >= 5].copy()
df = df.dropna()
print(f"\\nApos filtros (min 5 reviews + sem NAs): {len(df):,} vendedores")"""),

("markdown", "## 6. Resumo do dataset final"),

("code", """print(f"Shape: {df.shape}")
print(f"\\nY (n_negative):")
print(f"  Media:     {df['n_negative'].mean():.2f}")
print(f"  Mediana:   {df['n_negative'].median():.0f}")
print(f"  Variancia: {df['n_negative'].var():.2f}")
print(f"  Var/Media: {df['n_negative'].var()/df['n_negative'].mean():.2f}")
print(f"  Min: {df['n_negative'].min()}, Max: {df['n_negative'].max()}")
print(f"  Zeros: {(df['n_negative']==0).sum()} ({(df['n_negative']==0).mean()*100:.1f}%)")
print(f"\\nCategorias unicas: {df['categoria_principal'].nunique()}")
print(f"Estados unicos: {df['seller_state'].nunique()}")

df.describe()"""),

("markdown", "## 7. Salvar dataset"),

("code", """df.to_csv("../data/dataset_vendedores.csv", index=False)
print(f"Salvo: data/dataset_vendedores.csv ({len(df):,} vendedores, {len(df.columns)} colunas)")"""),
]

# =====================================================================
# 02 - EDA
# =====================================================================
nb02 = [
("markdown", """# 02 — Análise Exploratória dos Dados

Exploração da variável resposta e das variáveis explicativas."""),

("code", """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

df = pd.read_csv("../data/dataset_vendedores.csv")
print(f"Dataset: {len(df):,} vendedores")"""),

("markdown", "## 1. Distribuição da variável resposta"),

("code", """y = df["n_negative"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histograma
axes[0].hist(y, bins=range(0, min(int(y.quantile(0.95))+2, 50)), color="steelblue", edgecolor="white")
axes[0].set_xlabel("Reviews negativos")
axes[0].set_ylabel("Frequencia")
axes[0].set_title("Distribuicao de reviews negativos por vendedor")
axes[0].axvline(y.mean(), color="red", linestyle="--", label=f"Media={y.mean():.1f}")
axes[0].legend()

# Log scale
axes[1].hist(y[y > 0], bins=50, color="steelblue", edgecolor="white")
axes[1].set_xlabel("Reviews negativos")
axes[1].set_ylabel("Frequencia")
axes[1].set_title("Distribuicao (excluindo zeros)")
axes[1].set_yscale("log")

plt.tight_layout()
plt.savefig("../outputs/eda_distribuicao_negativos.png", bbox_inches="tight")
plt.show()

print(f"Media: {y.mean():.2f}, Variancia: {y.var():.2f}, Var/Media: {y.var()/y.mean():.2f}")
print(f"Zeros: {(y==0).sum()} ({(y==0).mean()*100:.1f}%)")"""),

("markdown", "## 2. Reviews negativos vs atraso de entrega"),

("code", """fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(df["atraso_medio"], df["n_negative"], alpha=0.3, s=10, color="steelblue")
axes[0].set_xlabel("Atraso medio (dias)")
axes[0].set_ylabel("Reviews negativos")
axes[0].set_title("Reviews negativos vs Atraso medio")

# Taxa de negativos vs atraso (binned)
df["atraso_bin"] = pd.cut(df["atraso_medio"], bins=10)
taxa = df.groupby("atraso_bin", observed=True).agg(
    taxa_neg=("n_negative", lambda x: x.sum()),
    n_reviews=("n_reviews", "sum")
).reset_index()
taxa["pct"] = taxa["taxa_neg"] / taxa["n_reviews"] * 100
axes[1].bar(range(len(taxa)), taxa["pct"], color="coral", edgecolor="white")
axes[1].set_xlabel("Faixa de atraso")
axes[1].set_ylabel("% reviews negativos")
axes[1].set_title("Taxa de reviews negativos por faixa de atraso")
axes[1].set_xticks(range(len(taxa)))
axes[1].set_xticklabels([str(x) for x in taxa["atraso_bin"]], rotation=45, ha="right", fontsize=7)

plt.tight_layout()
plt.savefig("../outputs/eda_negativos_vs_atraso.png", bbox_inches="tight")
plt.show()

print(f"Correlacao n_negative vs atraso_medio: {df['n_negative'].corr(df['atraso_medio']):.3f}")"""),

("markdown", "## 3. Reviews negativos por categoria"),

("code", """cat_stats = df.groupby("categoria_principal").agg(
    n_vendedores=("n_negative", "count"),
    neg_medio=("n_negative", "mean"),
    taxa_neg=("n_negative", lambda x: x.sum()),
    total_rev=("n_reviews", "sum")
).reset_index()
cat_stats["pct_neg"] = cat_stats["taxa_neg"] / cat_stats["total_rev"] * 100
cat_stats = cat_stats[cat_stats["n_vendedores"] >= 10].sort_values("pct_neg", ascending=False)

fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(cat_stats["categoria_principal"], cat_stats["pct_neg"], color="steelblue")
ax.set_xlabel("% reviews negativos")
ax.set_title("Taxa de reviews negativos por categoria (min 10 vendedores)")
ax.axvline(df["n_negative"].sum()/df["n_reviews"].sum()*100, color="red", linestyle="--", label="Media geral")
ax.legend()
plt.tight_layout()
plt.savefig("../outputs/eda_negativos_por_categoria.png", bbox_inches="tight")
plt.show()"""),

("markdown", "## 4. Reviews negativos por estado"),

("code", """state_stats = df.groupby("seller_state").agg(
    n_vendedores=("n_negative", "count"),
    taxa_neg=("n_negative", "sum"),
    total_rev=("n_reviews", "sum")
).reset_index()
state_stats["pct_neg"] = state_stats["taxa_neg"] / state_stats["total_rev"] * 100
state_stats = state_stats.sort_values("pct_neg", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].barh(state_stats["seller_state"], state_stats["pct_neg"], color="steelblue")
axes[0].set_xlabel("% reviews negativos")
axes[0].set_title("Taxa de negativos por estado")

axes[1].barh(state_stats["seller_state"], state_stats["n_vendedores"], color="coral")
axes[1].set_xlabel("Numero de vendedores")
axes[1].set_title("Vendedores por estado")

plt.tight_layout()
plt.savefig("../outputs/eda_negativos_por_estado.png", bbox_inches="tight")
plt.show()"""),

("markdown", "## 5. Correlações entre variáveis contínuas"),

("code", """cont_vars = ["n_negative", "n_reviews", "atraso_medio", "ticket_medio", "frete_medio", "peso_medio"]
corr = df[cont_vars].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, square=True, ax=ax)
ax.set_title("Matriz de correlacao")
plt.tight_layout()
plt.savefig("../outputs/eda_correlacao.png", bbox_inches="tight")
plt.show()"""),

("markdown", "## 6. Sobredispersão — verificação preliminar"),

("code", """media = y.mean()
variancia = y.var()
razao = variancia / media

print("=== Verificacao de sobredispersao ===")
print(f"Media:     {media:.2f}")
print(f"Variancia: {variancia:.2f}")
print(f"Razao V/M: {razao:.2f}")
print()
if razao > 1:
    print(f"Razao V/M = {razao:.2f} >> 1 --> Sobredispersao forte")
    print("Poisson inadequado. Binomial Negativa necessaria.")"""),
]

# =====================================================================
# 03 - MODELAGEM
# =====================================================================
nb03 = [
("markdown", """# 03 — Modelagem

Estimação dos modelos de Poisson e Binomial Negativa com offset de exposição.

**Offset:** log(n_reviews) — controla pela exposição de cada vendedor, modelando a **taxa** de negativos."""),

("code", """import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import json, warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("../data/dataset_vendedores.csv")
print(f"Dataset: {len(df):,} vendedores")"""),

("markdown", "## 1. Preparação das variáveis"),

("code", """# Agrupar categorias com menos de 30 vendedores
cat_counts = df["categoria_principal"].value_counts()
cats_keep = cat_counts[cat_counts >= 30].index.tolist()
df["cat_group"] = df["categoria_principal"].where(df["categoria_principal"].isin(cats_keep), "other")
print(f"Categorias: {df['categoria_principal'].nunique()} -> {df['cat_group'].nunique()} agrupadas")
print(df["cat_group"].value_counts())"""),

("code", """# Agrupar estados com menos de 30 vendedores
st_counts = df["seller_state"].value_counts()
st_keep = st_counts[st_counts >= 30].index.tolist()
df["state_group"] = df["seller_state"].where(df["seller_state"].isin(st_keep), "other")
print(f"Estados: {df['seller_state'].nunique()} -> {df['state_group'].nunique()} agrupados")
print(df["state_group"].value_counts())"""),

("code", """# Offset e dummies
df["log_n_reviews"] = np.log(df["n_reviews"])

df_model = df[["n_negative", "log_n_reviews", "atraso_medio", "ticket_medio",
               "frete_medio", "peso_medio", "cat_group", "state_group"]].copy()
df_model = pd.get_dummies(df_model, columns=["cat_group", "state_group"], drop_first=True, dtype=int)

y = df_model["n_negative"]
offset = df_model["log_n_reviews"]
X = df_model.drop(columns=["n_negative", "log_n_reviews"])
X = sm.add_constant(X)

print(f"Y: {y.shape}, X: {X.shape}")"""),

("markdown", "## 2. Modelo de Poisson"),

("code", """poisson = sm.GLM(y, X, family=sm.families.Poisson(), offset=offset).fit()
print(poisson.summary())"""),

("code", """print(f"Log-Likelihood: {poisson.llf:.2f}")
print(f"AIC: {poisson.aic:.2f}")
print(f"BIC: {poisson.bic_llf:.2f}")
print(f"Deviance: {poisson.deviance:.2f}")
print(f"Pearson chi2/df: {poisson.pearson_chi2/poisson.df_resid:.4f}  (>>1 indica sobredispersao)")"""),

("markdown", """## 3. Teste de sobredispersão (Cameron-Trivedi)

- H0: Equidispersão (Poisson adequado)
- H1: Sobredispersão (BN necessária)"""),

("code", """mu_hat = poisson.fittedvalues
aux_dep = ((y - mu_hat)**2 - y) / mu_hat
aux_X = sm.add_constant(mu_hat)
aux_ols = sm.OLS(aux_dep, aux_X).fit()

alpha_est = aux_ols.params.iloc[1]
t_stat = aux_ols.tvalues.iloc[1]
p_val_ct = aux_ols.pvalues.iloc[1]

print("=== Teste de Cameron-Trivedi ===")
print(f"Alpha estimado:  {alpha_est:.6f}")
print(f"Estatistica t:   {t_stat:.4f}")
print(f"p-valor:         {p_val_ct:.2e}")
if p_val_ct < 0.05 and alpha_est > 0:
    print("\\nRejeita H0: sobredispersao confirmada. BN necessaria.")
else:
    print("\\nNao rejeita H0: Poisson pode ser adequado.")"""),

("markdown", "## 4. Modelo Binomial Negativo"),

("code", """alpha_mm = max((poisson.pearson_chi2 / poisson.df_resid - 1) / mu_hat.mean(), 0.01)
print(f"Alpha (metodo dos momentos): {alpha_mm:.4f}")

negbin = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=alpha_mm), offset=offset).fit()
print(negbin.summary())"""),

("code", """print(f"Log-Likelihood: {negbin.llf:.2f}")
print(f"AIC: {negbin.aic:.2f}")
print(f"BIC: {negbin.bic_llf:.2f}")
print(f"Deviance: {negbin.deviance:.2f}")
print(f"Pearson chi2/df: {negbin.pearson_chi2/negbin.df_resid:.4f}")"""),

("markdown", "## 5. Comparação dos modelos"),

("code", """lr_stat = 2 * (negbin.llf - poisson.llf)
p_value_lr = stats.chi2.sf(abs(lr_stat), df=1)

print("=== Teste LR: Poisson vs BN ===")
print(f"LR stat: {abs(lr_stat):.2f}")
print(f"p-valor: {p_value_lr:.2e}")

fmt = "{:<20s} {:>15s} {:>15s} {:>10s}"
print("\\n" + fmt.format("Metrica", "Poisson", "NegBin", "Melhor"))
print("-" * 63)
for name, vp, vn, d in [
    ("Log-Likelihood", poisson.llf, negbin.llf, "maior"),
    ("AIC", poisson.aic, negbin.aic, "menor"),
    ("BIC", poisson.bic_llf, negbin.bic_llf, "menor"),
    ("Deviance", poisson.deviance, negbin.deviance, "menor"),
    ("Pearson chi2/df", poisson.pearson_chi2/poisson.df_resid,
     negbin.pearson_chi2/negbin.df_resid, "proximo_1"),
]:
    if d == "maior": m = "NegBin" if vn > vp else "Poisson"
    elif d == "menor": m = "NegBin" if vn < vp else "Poisson"
    else: m = "NegBin" if abs(vn-1) < abs(vp-1) else "Poisson"
    print(f"{name:<20s} {vp:>15.2f} {vn:>15.2f} {m:>10s}")"""),

("markdown", "## 6. Coeficientes e significância"),

("code", """coefs = pd.DataFrame({
    "coef": negbin.params, "std_err": negbin.bse,
    "z": negbin.tvalues, "p_value": negbin.pvalues,
    "exp_coef": np.exp(negbin.params)
})
coefs["sig"] = coefs["p_value"].apply(
    lambda p: "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else ""))
)

sig = coefs[coefs["p_value"] < 0.05]
nsig = coefs[coefs["p_value"] >= 0.05]

print(f"Significativas: {len(sig)}")
print(sig[["coef", "exp_coef", "p_value", "sig"]].to_string())
print(f"\\nNao significativas: {len(nsig)}")
if len(nsig) > 0:
    print(nsig[["coef", "exp_coef", "p_value"]].to_string())"""),

("markdown", "## 7. Modelo reduzido"),

("code", """vars_remover = [v for v in nsig.index.tolist() if v != "const"]

if len(vars_remover) > 0:
    print(f"Removendo {len(vars_remover)} variaveis nao significativas:")
    for v in vars_remover:
        print(f"  - {v} (p={coefs.loc[v, 'p_value']:.4f})")
    X_red = X.drop(columns=vars_remover)
    negbin_red = sm.GLM(y, X_red, family=sm.families.NegativeBinomial(alpha=alpha_mm), offset=offset).fit()
    print(f"\\nModelo Reduzido: {X_red.shape[1]} vars (vs {X.shape[1]})")
    print(f"AIC: {negbin_red.aic:.2f} (vs {negbin.aic:.2f})")
    print(f"BIC: {negbin_red.bic_llf:.2f} (vs {negbin.bic_llf:.2f})")
    print(negbin_red.summary())
else:
    print("Todas significativas. Modelo reduzido = completo.")
    negbin_red = negbin
    X_red = X"""),

("markdown", "## 8. Salvar resultados"),

("code", """coefs_final = pd.DataFrame({
    "coef": negbin_red.params, "std_err": negbin_red.bse,
    "z": negbin_red.tvalues, "p_value": negbin_red.pvalues,
    "exp_coef": np.exp(negbin_red.params)
})
coefs_final.to_csv("../outputs/coeficientes_negbin.csv")

metricas = {
    "poisson": {"aic": float(poisson.aic), "bic": float(poisson.bic_llf),
        "llf": float(poisson.llf), "deviance": float(poisson.deviance),
        "pearson_chi2_df": float(poisson.pearson_chi2/poisson.df_resid), "n_vars": int(X.shape[1])},
    "negbin_completo": {"aic": float(negbin.aic), "bic": float(negbin.bic_llf),
        "llf": float(negbin.llf), "deviance": float(negbin.deviance),
        "pearson_chi2_df": float(negbin.pearson_chi2/negbin.df_resid),
        "n_vars": int(X.shape[1]), "alpha": float(alpha_mm)},
    "negbin_reduzido": {"aic": float(negbin_red.aic), "bic": float(negbin_red.bic_llf),
        "llf": float(negbin_red.llf), "deviance": float(negbin_red.deviance),
        "pearson_chi2_df": float(negbin_red.pearson_chi2/negbin_red.df_resid),
        "n_vars": int(X_red.shape[1]), "alpha": float(alpha_mm)},
    "cameron_trivedi": {"alpha": float(alpha_est), "t": float(t_stat), "p_value": float(p_val_ct)},
    "lr_test": {"statistic": float(abs(lr_stat)), "p_value": float(p_value_lr)}
}
with open("../outputs/metricas_modelos.json", "w") as f:
    json.dump(metricas, f, indent=2)
print("Salvos: coeficientes_negbin.csv e metricas_modelos.json")"""),
]

# =====================================================================
# 04 - INTERPRETACAO
# =====================================================================
nb04 = [
("markdown", """# 04 — Interpretação dos Resultados

Interpretação dos coeficientes via exp(b) e diagnóstico do modelo."""),

("code", """import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import json, warnings
warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["figure.dpi"] = 100

df = pd.read_csv("../data/dataset_vendedores.csv")
coefs = pd.read_csv("../outputs/coeficientes_negbin.csv", index_col=0)
with open("../outputs/metricas_modelos.json") as f:
    metricas = json.load(f)

print(f"Dataset: {len(df):,} vendedores")
print(f"Coeficientes: {len(coefs)}")"""),

("markdown", """## 1. Interpretação via exp(b)

Com offset log(n_reviews), os coeficientes modelam a **taxa** de reviews negativos.
exp(b) indica o fator multiplicativo sobre a taxa para cada unidade de aumento em X."""),

("code", """coefs["pct_change"] = (coefs["exp_coef"] - 1) * 100

interp = coefs.drop(["const"], errors="ignore").copy()
interp = interp[interp["p_value"] < 0.05].sort_values("exp_coef", ascending=False)

print("=== Efeitos significativos ===")
fmt = "{:<40s} {:>8s} {:>8s} {:>10s} {:>10s}"
print(fmt.format("Variavel", "Coef", "exp(b)", "Efeito %", "p-valor"))
print("-" * 80)
for idx, row in interp.iterrows():
    sinal = "+" if row["pct_change"] > 0 else ""
    print(f"{idx:<40s} {row['coef']:>8.4f} {row['exp_coef']:>8.4f} {sinal}{row['pct_change']:>9.2f}% {row['p_value']:>10.2e}")"""),

("markdown", "## 2. Visualização dos coeficientes"),

("code", """interp_sorted = interp.sort_values("coef")

fig, axes = plt.subplots(1, 2, figsize=(14, max(5, len(interp_sorted)*0.5)))

colors = ["steelblue" if c > 0 else "coral" for c in interp_sorted["coef"]]
axes[0].barh(interp_sorted.index, interp_sorted["coef"], color=colors, edgecolor="white")
axes[0].axvline(0, color="black", linewidth=0.5)
axes[0].set_xlabel("Coeficiente (b)")
axes[0].set_title("Coeficientes significativos")

colors2 = ["steelblue" if c > 1 else "coral" for c in interp_sorted["exp_coef"]]
axes[1].barh(interp_sorted.index, interp_sorted["exp_coef"], color=colors2, edgecolor="white")
axes[1].axvline(1, color="black", linewidth=0.5, linestyle="--")
axes[1].set_xlabel("exp(b)")
axes[1].set_title("Fator multiplicativo sobre taxa de negativos")

plt.tight_layout()
plt.savefig("../outputs/interp_coeficientes.png", bbox_inches="tight")
plt.show()"""),

("markdown", "## 3. Tabela comparativa"),

("code", """print("=== Comparacao final ===")
fmt = "{:<20s} {:>15s} {:>15s} {:>15s}"
print(fmt.format("", "Poisson", "BN Completo", "BN Reduzido"))
print("-" * 68)
for key, label in [("aic", "AIC"), ("bic", "BIC"), ("llf", "Log-Likelihood"), ("deviance", "Deviance")]:
    vp = metricas["poisson"][key]
    vc = metricas["negbin_completo"][key]
    vr = metricas["negbin_reduzido"][key]
    print(f"{label:<20s} {vp:>15.2f} {vc:>15.2f} {vr:>15.2f}")

ct = metricas["cameron_trivedi"]
print(f"\\nCameron-Trivedi: alpha={ct['alpha']:.4f}, t={ct['t']:.2f}, p={ct['p_value']:.2e}")
lr = metricas["lr_test"]
print(f"LR test: stat={lr['statistic']:.2f}, p={lr['p_value']:.2e}")"""),

("markdown", "## 4. Diagnóstico dos resíduos"),

("code", """# Reestimar modelo
cat_counts = df["categoria_principal"].value_counts()
cats_keep = cat_counts[cat_counts >= 30].index.tolist()
df["cat_group"] = df["categoria_principal"].where(df["categoria_principal"].isin(cats_keep), "other")

st_counts = df["seller_state"].value_counts()
st_keep = st_counts[st_counts >= 30].index.tolist()
df["state_group"] = df["seller_state"].where(df["seller_state"].isin(st_keep), "other")

df["log_n_reviews"] = np.log(df["n_reviews"])
df_model = df[["n_negative", "log_n_reviews", "atraso_medio", "ticket_medio",
               "frete_medio", "peso_medio", "cat_group", "state_group"]].copy()
df_model = pd.get_dummies(df_model, columns=["cat_group", "state_group"], drop_first=True, dtype=int)

y = df_model["n_negative"]
offset = df_model["log_n_reviews"]
X = df_model.drop(columns=["n_negative", "log_n_reviews"])
X = sm.add_constant(X)

alpha_mm = metricas["negbin_completo"]["alpha"]
nb = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=alpha_mm), offset=offset).fit()
y_pred = nb.fittedvalues
residuos = y - y_pred

mask = np.isfinite(residuos) & np.isfinite(y_pred)
res_plot = residuos[mask]
pred_plot = y_pred[mask]
y_plot = y[mask]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].scatter(pred_plot, res_plot, alpha=0.3, s=10, color="steelblue")
axes[0,0].axhline(0, color="red", linewidth=0.5)
axes[0,0].set_xlabel("Valores ajustados")
axes[0,0].set_ylabel("Residuos")
axes[0,0].set_title("Residuos vs Ajustados")

axes[0,1].hist(res_plot, bins=50, color="steelblue", edgecolor="white", density=True)
axes[0,1].set_xlabel("Residuo")
axes[0,1].set_title("Distribuicao dos residuos")

stats.probplot(res_plot, plot=axes[1,0])
axes[1,0].set_title("QQ Plot")

axes[1,1].scatter(y_plot, pred_plot, alpha=0.3, s=10, color="steelblue")
lim = max(y_plot.max(), pred_plot.max())
axes[1,1].plot([0, lim], [0, lim], "r--", linewidth=0.5)
axes[1,1].set_xlabel("Real")
axes[1,1].set_ylabel("Previsto")
axes[1,1].set_title("Real vs Previsto")

plt.suptitle("Diagnostico - Binomial Negativa", fontsize=13)
plt.tight_layout()
plt.savefig("../outputs/interp_diagnostico_residuos.png", bbox_inches="tight")
plt.show()"""),

("markdown", "## 5. Resumo"),

("code", """print("=" * 60)
print("RESUMO DOS RESULTADOS")
print("=" * 60)

print(f"\\n1. SOBREDISPERSAO")
print(f"   Var/Media = {y.var()/y.mean():.2f}")
print(f"   Cameron-Trivedi p = {metricas['cameron_trivedi']['p_value']:.2e}")

print(f"\\n2. MODELO SELECIONADO: Binomial Negativa")
print(f"   AIC: {metricas['negbin_reduzido']['aic']:.2f}")
print(f"   BIC: {metricas['negbin_reduzido']['bic']:.2f}")
print(f"   Pearson chi2/df: {metricas['negbin_reduzido']['pearson_chi2_df']:.4f}")

print(f"\\n3. DETERMINANTES DA INSATISFACAO")
for idx, row in interp.iterrows():
    direcao = "AUMENTA" if row["pct_change"] > 0 else "REDUZ"
    print(f"   {idx}: {direcao} {abs(row['pct_change']):.1f}% a taxa de reviews negativos")"""),
]

# =====================================================================
# GERAR
# =====================================================================
print("Gerando notebooks:")
make_nb(nb01, "01_preparacao.ipynb")
make_nb(nb02, "02_eda.ipynb")
make_nb(nb03, "03_modelagem.ipynb")
make_nb(nb04, "04_interpretacao.ipynb")
print("OK")
