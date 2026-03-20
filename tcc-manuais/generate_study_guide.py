from fpdf import FPDF

class StudyGuide(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, 'Guia de Estudos - TCC Data Science e Analytics | USP/Esalq - PECEGE', align='C')
        self.ln(10)
        self.set_draw_color(200, 200, 200)
        self.line(10, 18, 200, 18)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(25, 60, 120)
        self.ln(4)
        self.cell(0, 10, title)
        self.ln(10)
        self.set_draw_color(25, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=15):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.set_x(indent)
        self.cell(5, 5.5, '-')
        self.multi_cell(0, 5.5, text)
        self.ln(0.5)

    def ref_item(self, pages, title, desc):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(25, 60, 120)
        self.cell(0, 6, f'pp. {pages} - {title}')
        self.ln(6)
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(60, 60, 60)
        self.set_x(20)
        self.multi_cell(0, 5, desc)
        self.ln(2)

    def concept_box(self, title, desc):
        self.set_fill_color(240, 245, 255)
        self.set_draw_color(25, 60, 120)
        y_start = self.get_y()
        self.set_x(15)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(25, 60, 120)
        self.cell(0, 6, title)
        self.ln(7)
        self.set_x(15)
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(50, 50, 50)
        self.multi_cell(180, 5, desc)
        y_end = self.get_y() + 2
        self.rect(12, y_start - 2, 186, y_end - y_start + 4)
        self.ln(4)


pdf = StudyGuide()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ===== COVER PAGE =====
pdf.add_page()
pdf.ln(40)
pdf.set_font('Helvetica', 'B', 24)
pdf.set_text_color(25, 60, 120)
pdf.cell(0, 15, 'Guia de Estudos', align='C')
pdf.ln(18)
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, 'para o Trabalho de Conclusao de Curso', align='C')
pdf.ln(15)
pdf.set_draw_color(25, 60, 120)
pdf.line(50, pdf.get_y(), 160, pdf.get_y())
pdf.ln(12)
pdf.set_font('Helvetica', 'I', 12)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(0, 7, '"Previsao diaria de pedidos em e-commerce\ncom regressao binomial negativa"', align='C')
pdf.ln(20)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 7, 'Aluno: Maycon Henrique Aranha da Silva', align='C')
pdf.ln(8)
pdf.cell(0, 7, 'Orientador: Gustavo Dantas Lobo', align='C')
pdf.ln(8)
pdf.cell(0, 7, 'MBA Data Science e Analytics - USP/Esalq (PECEGE)', align='C')
pdf.ln(8)
pdf.cell(0, 7, '2o Semestre 2025', align='C')

# ===== PAGE 2: OVERVIEW =====
pdf.add_page()
pdf.section_title('1. Visao Geral do Projeto')
pdf.body_text(
    'Este guia organiza os topicos e referencias que voce precisa estudar para desenvolver '
    'o TCC sobre previsao de demanda em e-commerce usando Regressao Binomial Negativa. '
    'O roteiro esta alinhado com a metodologia proposta no Projeto de Pesquisa e com o cronograma de atividades.'
)
pdf.ln(2)
pdf.sub_title('Resumo da pesquisa')
pdf.bullet('Variavel resposta: numero diario de pedidos (variavel de contagem)')
pdf.bullet('Modelo principal: Regressao Binomial Negativa com regressoras de calendario e lags')
pdf.bullet('Baseline: mediana sazonal semanal (ultimas 4 semanas)')
pdf.bullet('Validacao: backtesting rolling one-step ahead com janela expansivel (60 dias)')
pdf.bullet('Metricas: wMAPE e sMAPE')
pdf.bullet('Dados: Olist (Kaggle) - olist_orders_dataset.csv')
pdf.bullet('Linguagem: Python')

pdf.ln(3)
pdf.sub_title('Mapa de competencias necessarias')
pdf.body_text(
    'Para executar este projeto com solidez, voce precisa dominar 4 areas de conhecimento:'
)
pdf.bullet('(A) Modelos de regressao para dados de contagem (Poisson e Binomial Negativa)')
pdf.bullet('(B) Deteccao e tratamento de sobredispersao')
pdf.bullet('(C) Validacao temporal e metricas de previsao')
pdf.bullet('(D) Engenharia de features temporais (calendario, lags, feriados)')

# ===== FAVERO TEXTBOOK =====
pdf.add_page()
pdf.section_title('2. Favero e Belfiore (2017) - Manual de Analise de Dados')
pdf.body_text(
    'REFERENCIA PRINCIPAL para a fundamentacao teorica do modelo. '
    'O Capitulo 14 e inteiramente dedicado a modelos de contagem e cobre Poisson e Binomial Negativo '
    'com resolucao algebrica e em software.'
)
pdf.ln(2)

pdf.sub_title('Capitulo 14 - Modelos de Regressao para Dados de Contagem (pp. 695-780)')
pdf.body_text('Este e o capitulo mais importante para o seu TCC. Estude-o integralmente.')
pdf.ln(1)

pdf.ref_item('695-696', '14.1 Introducao',
    'Contextualizacao de quando usar modelos de contagem. Entenda por que regressao linear '
    'nao e apropriada para variaveis de contagem (numeros inteiros nao negativos).')

pdf.ref_item('697-709', '14.2 Modelo de Regressao Poisson',
    'Fundamento do modelo de Poisson: distribuicao, funcao de ligacao logaritmica, '
    'estimacao por maxima verossimilhanca (MV), significancia estatistica (teste de Wald, '
    'razao de verossimilhanca), intervalos de confianca. ESSENCIAL entender antes de '
    'avancar para a Binomial Negativa.')

pdf.ref_item('710-711', '14.2.4 Teste para verificacao de superdispersao',
    'CRITICO para o TCC. Explica como detectar quando a variancia excede a media '
    '(superdispersao), invalidando o pressuposto de equidispersao do Poisson. '
    'Este teste justifica a escolha da Binomial Negativa no seu projeto.')

pdf.ref_item('712-723', '14.3 Modelo de Regressao Binomial Negativo',
    'NUCLEO DO SEU TCC. Cobre: distribuicao binomial negativa, parametro de dispersao (phi), '
    'estimacao por MV (14.3.1, pp. 715-719), significancia (14.3.2, pp. 720-722), '
    'intervalos de confianca (14.3.3, pp. 723). Domine a interpretacao dos coeficientes.')

pdf.ref_item('724-745', '14.4 Estimacao no software Stata',
    'Embora voce use Python, a logica de estimacao e identica. Leia para entender os '
    'outputs tipicos: log-likelihood, AIC, BIC, teste de Wald, e a comparacao Poisson vs BN.')

pdf.ref_item('771-780', 'Apendice - Modelos inflacionados de zeros',
    'Leitura complementar. Se a sua serie tiver muitos dias com zero pedidos, '
    'pode ser necessario considerar um modelo ZIP ou ZINB. Tenha isso como contingencia.')

pdf.ln(2)
pdf.sub_title('Capitulos complementares do Favero')
pdf.bullet('Cap. 5 - Distribuicoes de probabilidade (pp. 137-166): revisao de Poisson, Gama e distribuicoes discretas')
pdf.bullet('Cap. 7 - Testes de hipoteses (pp. 191-240): fundamentos do teste de razao de verossimilhanca')
pdf.bullet('Cap. 12 - Regressao simples e multipla (pp. 511-600): variaveis dummy (12.2.6, p. 541)')

# ===== CAMERON & TRIVEDI =====
pdf.add_page()
pdf.section_title('3. Cameron e Trivedi (2013) - Regression Analysis of Count Data')
pdf.body_text(
    'Referencia fundamental e avancada sobre modelos de contagem. E a obra que '
    'fundamenta o teste de razao de verossimilhanca (LR test) para comparar Poisson vs Binomial Negativa.'
)
pdf.ln(2)

pdf.sub_title('Capitulos prioritarios')
pdf.ref_item('Cap. 1-2', 'Introduction e Count Data: Basic Setup',
    'Visao geral de dados de contagem, propriedades da distribuicao de Poisson, '
    'a distribuicao Binomial Negativa como alternativa. Motivacao para modelos de contagem.')

pdf.ref_item('Cap. 3', 'Basic Count Regression (Poisson)',
    'Modelo de Poisson como baseline. Estimacao por MV. Interpretacao de coeficientes '
    'como taxas de incidencia (IRR). Diagnosticos de ajuste.')

pdf.ref_item('Cap. 4', 'Generalized Count Regression',
    'ESSENCIAL. Extensoes do Poisson para lidar com sobredispersao: Binomial Negativa (NB1 e NB2), '
    'modelos quasi-Poisson. Entenda a diferenca entre NB1 (variancia linear) e NB2 (variancia quadratica) - '
    'o NB2 e o mais comum e provavelmente o que voce usara no Python (statsmodels).')

pdf.ref_item('Cap. 5, pp. 139-188', 'Model Evaluation and Testing',
    'CRITICO. Testes de especificacao: teste de razao de verossimilhanca (LR test) '
    'para comparar Poisson vs NB. O LR test tem distribuicao nao padrao (mistura de '
    'massa pontual em zero e meia chi-quadrado). Cameron e Trivedi sao os autores '
    'que formalizaram os testes de sobredispersao mais utilizados.')

# ===== HILBE =====
pdf.add_page()
pdf.section_title('4. Hilbe (2011) - Negative Binomial Regression')
pdf.body_text(
    'A monografia definitiva sobre Regressao Binomial Negativa. Complementa Cameron e Trivedi '
    'com foco exclusivo na BN. Use como referencia de consulta para questoes especificas.'
)
pdf.ln(2)

pdf.sub_title('Capitulos prioritarios')
pdf.ref_item('Cap. 1', 'Introduction to Count Regression',
    'Historico da distribuicao de Poisson e da Binomial Negativa. Definicoes formais.')

pdf.ref_item('Cap. 4-5', 'Negative Binomial Regression (NB2 e NB1)',
    'Detalhamento dos dois tipos principais de BN. O NB2 (Cap. 4) e o padrao na maioria '
    'dos softwares. Estimacao, interpretacao, diagnosticos. Leia especialmente sobre o '
    'parametro de heterogeneidade (alpha) e sua interpretacao.')

pdf.ref_item('Cap. 7', 'Negative Binomial Regression: Modeling',
    'Estrategias praticas de modelagem: selecao de variaveis, diagnosticos de ajuste, '
    'residuos, influencia. Util para a fase de estimacao do seu modelo.')

pdf.ref_item('Cap. 10-11', 'Problems with Count Models / Generalized Models',
    'Problemas comuns: excesso de zeros, subdispersao, truncamento. '
    'Importante para saber quando a BN padrao pode nao ser suficiente.')

# ===== FAVERO ET AL 2024 =====
pdf.ln(4)
pdf.section_title('5. Favero et al. (2024) - Algoritmo para Sobredispersao')
pdf.body_text(
    'Artigo recente (open access: mdpi.com/2073-431X/13/4/88) que implementa em Python um '
    'algoritmo para detectar sobredispersao e inflacao de zeros em modelos de contagem. '
    'Diretamente aplicavel ao seu projeto.'
)
pdf.ln(2)
pdf.sub_title('O que estudar neste artigo')
pdf.bullet('Secao 2: Overview of Count Data - revisao concisa de Poisson, BN e modelos inflacionados de zeros')
pdf.bullet('Secao 3: Likelihood Ratio Test - implementacao do teste LR para sobredispersao')
pdf.bullet('Secao 4: Vuong Test - teste de selecao entre modelos aninhados e nao aninhados')
pdf.bullet('Secao 5: Python Algorithm - codigo que voce pode adaptar/referenciar na sua implementacao')
pdf.ln(2)
pdf.body_text(
    'DICA PRATICA: O artigo disponibiliza codigo Python que pode servir como referencia '
    'para implementar o teste de sobredispersao no seu notebook. Use statsmodels para '
    'estimar os modelos e aplique o LR test conforme descrito no artigo.'
)

# ===== HYNDMAN =====
pdf.add_page()
pdf.section_title('6. Hyndman e Athanasopoulos (2021) - Forecasting: Principles and Practice')
pdf.body_text(
    'Livro-texto de previsao, disponivel gratuitamente em otexts.com/fpp3. '
    'Cobre os fundamentos de avaliacao de previsoes que voce precisa para a validacao do modelo.'
)
pdf.ln(2)

pdf.sub_title('Capitulos prioritarios')
pdf.ref_item('Cap. 1', 'Getting Started',
    'Introducao a previsao. Tipos de dados temporais. O pipeline de um projeto de forecasting.')

pdf.ref_item('Cap. 2', 'Time Series Graphics',
    'Padroes temporais: tendencia, sazonalidade, ciclos. Use para a analise exploratoria '
    'da sua serie de pedidos (identificar sazonalidade semanal, feriados, etc.).')

pdf.ref_item('Cap. 3', 'Time Series Decomposition',
    'Decomposicao de series. Util para entender os componentes da sua serie de pedidos.')

pdf.ref_item('Cap. 5', 'The Forecasters Toolbox',
    'ESSENCIAL. Metricas de acuracia (MAE, MAPE, sMAPE) e estrategias de avaliacao. '
    'Aqui voce encontra a fundamentacao para wMAPE e sMAPE usados no seu projeto. '
    'Secao 5.8 sobre avaliacao com conjuntos de teste temporais (time series cross-validation) '
    'fundamenta o seu backtesting rolling one-step ahead.')

pdf.ref_item('Cap. 7', 'Time Series Regression Models',
    'Modelos de regressao com componentes temporais. Variaveis dummy para sazonalidade, '
    'feriados, e efeitos de calendario. Diretamente relevante para as suas regressoras.')

pdf.ln(3)
pdf.sub_title('Recurso adicional')
pdf.body_text(
    'O livro tem versao interativa com codigo em R. Embora voce use Python, os conceitos '
    'e formulas sao identicos. Para implementacao Python, consulte a biblioteca sktime ou '
    'implemente as metricas manualmente (recomendado para demonstrar dominio no TCC).'
)

# ===== FILDES + MAKRIDAKIS =====
pdf.add_page()
pdf.section_title('7. Fildes et al. (2022) e Makridakis et al. (2022)')
pdf.sub_title('Fildes, Ma e Kolassa (2022) - Retail Forecasting: Research and Practice')
pdf.body_text(
    'Artigo de revisao sobre o estado da arte em previsao para varejo. '
    'International Journal of Forecasting, 38, 1283-1318.'
)
pdf.ln(1)
pdf.bullet('Secao 2: panorama dos metodos de previsao usados em varejo')
pdf.bullet('Secao 3: desafios especificos (dados esparsos, promocoes, novos produtos)')
pdf.bullet('Secao 5: lacunas entre pesquisa academica e pratica - bom para contextualizar na Introducao')
pdf.ln(2)
pdf.body_text(
    'Este artigo justifica POR QUE previsao de demanda em e-commerce e relevante e quais '
    'desafios praticos existem. Use-o para fortalecer a Introducao do TCC.'
)

pdf.ln(4)
pdf.sub_title('Makridakis, Spiliotis e Assimakopoulos (2022) - M5 Competition')
pdf.body_text(
    'Resultados da competicao M5 (Kaggle) com dados reais do Walmart. '
    'International Journal of Forecasting, 38(4), 1346-1364.'
)
pdf.ln(1)
pdf.bullet('Usou 42.840 series temporais reais de vendas do Walmart')
pdf.bullet('Top metodos (LightGBM, XGBoost) superaram benchmarks estatisticos em ~22%')
pdf.bullet('Apenas 7,5% dos participantes superaram o baseline de suavizacao exponencial')
pdf.bullet('Conclusao: metodos hibridos (ML + features de calendario) tendem a superar baselines simples')
pdf.ln(2)
pdf.body_text(
    'Este artigo reforca a motivacao do seu projeto: modelos que incorporam features de '
    'calendario e padroes historicos podem superar baselines simples - exatamente a hipotese que voce testa.'
)

# ===== CONCEPTS =====
pdf.add_page()
pdf.section_title('8. Conceitos-Chave para Dominar')
pdf.body_text(
    'Abaixo estao os conceitos fundamentais que voce precisa dominar. Para cada um, '
    'indico a referencia primaria.'
)
pdf.ln(3)

pdf.concept_box('Distribuicao de Poisson',
    'Distribuicao discreta para contagem de eventos. Pressuposto: media = variancia (equidispersao). '
    'E(Y) = Var(Y) = lambda. Quando este pressuposto falha, temos sobredispersao. '
    '(Favero Cap. 14.2; Cameron Cap. 3)')

pdf.concept_box('Sobredispersao (Overdispersion)',
    'Quando Var(Y) > E(Y). Causa: heterogeneidade nao observada, excesso de zeros, ou '
    'correlacao entre eventos. Consequencia: erros-padrao subestimados no Poisson, levando '
    'a significancias espurias. Deteccao: teste LR ou teste de Cameron-Trivedi. '
    '(Favero 14.2.4; Cameron Cap. 5; Favero et al. 2024)')

pdf.concept_box('Regressao Binomial Negativa (NB2)',
    'Extensao do Poisson com parametro de dispersao alpha > 0. '
    'Var(Y) = mu + alpha * mu^2. Quando alpha -> 0, converge para Poisson. '
    'Estimacao por maxima verossimilhanca. O teste H0: alpha=0 via LR test '
    'decide entre Poisson e BN. (Favero Cap. 14.3; Hilbe Cap. 4; Cameron Cap. 4)')

pdf.concept_box('Teste de Razao de Verossimilhanca (LR Test)',
    'Compara o ajuste de dois modelos aninhados: LR = 2*(LL_completo - LL_restrito). '
    'No caso Poisson vs BN: H0: alpha=0 (Poisson suficiente). '
    'Distribuicao sob H0: mistura 0.5*chi2(0) + 0.5*chi2(1). '
    'p-valor = 0.5 * P(chi2(1) > LR). (Cameron Cap. 5; Favero et al. 2024)')

pdf.concept_box('Variaveis Dummy de Calendario',
    'Indicadores binarios para capturar padroes sazonais: dia da semana (6 dummies, '
    'domingo como referencia), feriados nacionais, efeito payday (dias 5 e 20 + 2 dias uteis). '
    'Fundamentacao: features de calendario sao standard em previsao de varejo. '
    '(Hyndman Cap. 7; Fildes et al. 2022)')

pdf.concept_box('Lags Historicos como Regressoras',
    'Valores passados da variavel resposta: lag1 (ontem), lag7 (mesmo dia semana passada), '
    'lag14 (mesmo dia ha 2 semanas). Capturam autocorrelacao serial e padroes recorrentes. '
    'Cuidado: lags introduzem dependencia temporal na estimacao. '
    '(Hyndman Cap. 7)')

pdf.add_page()
pdf.section_title('8. Conceitos-Chave (continuacao)')

pdf.concept_box('Backtesting Rolling One-Step Ahead',
    'Estrategia de validacao temporal: a cada dia t no periodo de teste (60 dias), '
    'reestima o modelo com dados [1, t-1] e preve t. Janela expansivel = o conjunto '
    'de treino cresce a cada iteracao. Evita data leakage temporal. '
    '(Hyndman Cap. 5, Secao 5.8 - Time Series Cross-Validation)')

pdf.concept_box('wMAPE (weighted Mean Absolute Percentage Error)',
    'wMAPE = sum(|y_t - yhat_t|) / sum(y_t). Pondera pelo volume real, evitando '
    'distorcoes de dias com poucos pedidos. Mais robusto que MAPE para series '
    'com valores proximos de zero. (Hyndman Cap. 5)')

pdf.concept_box('sMAPE (symmetric Mean Absolute Percentage Error)',
    'sMAPE = (1/n) * sum(2*|y_t - yhat_t| / (|y_t| + |yhat_t|)). '
    'Simetrico entre sobre e subestimacao. Varia de 0% (perfeito) a 200% (pior caso). '
    'Amplamente usado em competicoes de previsao (M3, M4, M5). (Hyndman Cap. 5; Makridakis et al. 2022)')

pdf.concept_box('Baseline Sazonal Semanal',
    'Modelo de referencia simples: previsao = mediana dos pedidos no mesmo dia da semana '
    'nas 4 semanas anteriores. Captura sazonalidade semanal sem modelagem parametrica. '
    'Todo modelo proposto deve ser comparado a um baseline interpretavel. (Hyndman Cap. 5)')

# ===== STUDY ROADMAP =====
pdf.add_page()
pdf.section_title('9. Roteiro de Estudo Sugerido')
pdf.body_text(
    'Organize seus estudos nas seguintes fases, alinhadas ao cronograma do Projeto de Pesquisa:'
)
pdf.ln(3)

pdf.sub_title('Fase 1 - Fundamentacao Teorica (Abril-Maio)')
pdf.bullet('Estudar Favero Cap. 14 integralmente (pp. 695-780) - 2 a 3 semanas')
pdf.bullet('Ler Cameron & Trivedi Cap. 3-5 (foco nos Cap. 4-5) - 1 a 2 semanas')
pdf.bullet('Ler Fildes et al. (2022) e Makridakis et al. (2022) para contextualizar - 2 dias')
pdf.bullet('Revisar Hyndman Cap. 1-3 e Cap. 7 sobre features temporais - 1 semana')

pdf.ln(2)
pdf.sub_title('Fase 2 - Implementacao (Maio-Julho)')
pdf.bullet('Estudar Favero et al. (2024) - algoritmo de sobredispersao em Python - 2 dias')
pdf.bullet('Implementar pipeline de dados: leitura Olist, filtros, serie diaria')
pdf.bullet('Implementar teste de sobredispersao (LR test) com statsmodels')
pdf.bullet('Estimar modelo BN com statsmodels (NegativeBinomial ou GLM)')
pdf.bullet('Implementar baseline sazonal e backtesting rolling')
pdf.bullet('Consultar Hilbe Cap. 4-5 e 7 para duvidas sobre modelagem')

pdf.ln(2)
pdf.sub_title('Fase 3 - Avaliacao e Redacao (Julho-Setembro)')
pdf.bullet('Calcular wMAPE e sMAPE - consultar Hyndman Cap. 5 para fundamentacao')
pdf.bullet('Comparar modelo BN vs baseline e interpretar resultados')
pdf.bullet('Redigir TCC seguindo template e normas USP/Esalq')
pdf.bullet('Revisitar Cameron & Trivedi e Hilbe para fundamentar a discussao')

pdf.ln(2)
pdf.sub_title('Fase 4 - Revisao e Defesa (Setembro-Outubro)')
pdf.bullet('Revisar formatacao conforme Manual de Instrucoes e Normas')
pdf.bullet('Preparar slides (20 min) focando em: problema, metodo, resultados, conclusao')
pdf.bullet('Praticar defesa e antecipacao de perguntas da banca')

# ===== PYTHON LIBS =====
pdf.add_page()
pdf.section_title('10. Ferramentas Python Recomendadas')
pdf.body_text('Bibliotecas que voce usara no projeto:')
pdf.ln(3)

pdf.sub_title('Manipulacao de dados')
pdf.bullet('pandas - leitura CSV, agregacao temporal, criacao de features')
pdf.bullet('numpy - operacoes numericas')

pdf.ln(1)
pdf.sub_title('Modelagem estatistica')
pdf.bullet('statsmodels.discrete.count_model.NegativeBinomial - modelo BN')
pdf.bullet('statsmodels.genmod.generalized_linear_model.GLM (family=NegativeBinomial) - alternativa via GLM')
pdf.bullet('statsmodels.discrete.count_model.Poisson - modelo Poisson (para comparacao)')
pdf.bullet('scipy.stats.chi2 - para calcular p-valor do LR test')

pdf.ln(1)
pdf.sub_title('Features de calendario')
pdf.bullet('holidays (pip install holidays) - feriados nacionais brasileiros')
pdf.bullet('pandas.Categorical / pd.get_dummies - dummies de dia da semana')

pdf.ln(1)
pdf.sub_title('Visualizacao')
pdf.bullet('matplotlib / seaborn - graficos da serie, residuos, comparacoes')

pdf.ln(1)
pdf.sub_title('Validacao')
pdf.bullet('Implementacao manual do backtesting rolling (loop com reestimacao)')
pdf.bullet('sklearn.metrics ou implementacao manual de wMAPE e sMAPE')

pdf.ln(5)
pdf.set_draw_color(25, 60, 120)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(5)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5.5,
    'Este guia foi elaborado com base nos manuais do curso e nas referencias do Projeto de Pesquisa. '
    'Foque nos capitulos indicados como prioritarios e avance para os complementares conforme necessidade.'
)

# Save
output_path = r'C:\Users\Maycon\Desktop\workspace\tcc-statmodel\Guia_de_Estudos_TCC.pdf'
pdf.output(output_path)
print(f'PDF gerado: {output_path}')
print(f'Total de paginas: {pdf.page_no()}')
