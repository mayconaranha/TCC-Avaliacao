# Descobertas e Notas para Redação do TCC

> Arquivo de referência com achados da análise exploratória e modelagem.
> Útil para embasar a seção de Resultados e Discussão.

---

## Dados e Amostra

- Base Olist: 7 datasets combinados (pedidos, itens, pagamentos, reviews, produtos, vendedores, tradução de categorias)
- Unidade de análise: **vendedor** (agregação por `seller_id`)
- Filtro: vendedores com no mínimo 5 reviews
- Amostra final: **1.754 vendedores**
- Variável dependente: contagem de reviews negativos (score 1 ou 2) por vendedor
- Offset: log(total de reviews) — modelo estima a **taxa** de insatisfação, não a contagem absoluta

## Análise Exploratória

- Distribuição de Y altamente concentrada à esquerda (muitos vendedores com poucos reviews negativos)
- Razão Variância/Média = **52,90** — sobredispersão severa, Poisson inadequado
- Atraso médio na entrega é o fator mais visualmente correlacionado com reviews negativos
- 19 categorias de produto agrupadas (threshold 30 vendedores) + grupo "other"
- 7 grupos de estado (SP, MG, RJ, PR, SC, RS + "other")

## Teste de Sobredispersão (Cameron-Trivedi)

- Alpha estimado: 0,0449
- Estatística t: 6,29
- **p-valor: 3,88 × 10⁻¹⁰**
- Conclusão: rejeita H₀ de equidispersão. Modelo Binomial Negativo é necessário.

## Comparação Poisson vs Binomial Negativa

| Métrica         | Poisson   | BN Completo | BN Reduzido |
|-----------------|-----------|-------------|-------------|
| AIC             | 7.488,67  | 6.996,66    | **6.982,97** |
| BIC             | 7.647,29  | 7.155,28    | **7.015,78** |
| Log-Likelihood  | −3.715,34 | −3.469,33   | −3.485,48   |
| Deviance        | 3.002,79  | 1.831,60    | 1.863,90    |
| Pearson χ²/df   | 1,79      | 1,05        | **1,06**     |

- Teste LR (Poisson vs BN): estatística = 492,01, p = 5,21 × 10⁻¹⁰⁹
- BN Reduzido é o modelo selecionado (menor AIC e BIC, Pearson χ²/df próximo de 1)

## Modelo Final: BN Reduzido (5 variáveis significativas)

| Variável              | Coeficiente | exp(b) | Efeito (%)   | p-valor      |
|-----------------------|-------------|--------|--------------|--------------|
| atraso_medio          | 0,0436      | 1,0445 | **+4,45%/dia**  | 9,16 × 10⁻²⁵ |
| frete_medio           | 0,0054      | 1,0054 | **+0,54%/R$**   | 3,65 × 10⁻¹⁰ |
| cat_telephony         | 0,3051      | 1,3568 | **+35,7%**      | 2,06 × 10⁻⁴  |
| cat_bed_bath_table    | 0,2706      | 1,3108 | **+31,1%**      | 3,03 × 10⁻⁶  |
| cat_furniture_decor   | 0,2387      | 1,2696 | **+27,0%**      | 2,99 × 10⁻⁵  |

### Interpretação

- **Atraso na entrega** é o principal determinante: cada dia adicional de atraso médio aumenta em 4,45% a taxa esperada de reviews negativos. É a variável com maior significância estatística (p ≈ 10⁻²⁵).
- **Frete** tem efeito pequeno mas altamente significativo: cada R$1 a mais no frete médio aumenta 0,54% a taxa de insatisfação.
- **Categorias de risco**: telefonia (+35,7%), cama/mesa/banho (+31,1%) e móveis/decoração (+27,0%) apresentam taxas significativamente maiores de insatisfação em relação à categoria base (esportes/lazer).
- **Variáveis não significativas**: ticket médio, peso médio, todas as demais categorias e todos os estados. Nenhum estado brasileiro apresentou diferença significativa na taxa de insatisfação.

## Variáveis Removidas (p ≥ 0,05)

23 variáveis removidas no modelo reduzido: ticket_medio, peso_medio, 16 dummies de categoria, 6 dummies de estado. A remoção melhorou AIC (de 6.996 para 6.983) e BIC (de 7.155 para 7.016).

## Qualidade do Ajuste

- Pearson χ²/df = 1,06 (ideal ≈ 1,00) — ajuste excelente
- Pseudo R² (CS) = 0,10 — típico de modelos de contagem com dados cross-section
- Resíduos sem padrões sistemáticos nos gráficos diagnósticos
