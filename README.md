# ⚡ DATA STORM · Análise Preditiva de Sífilis Congênita em MG

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![Status](https://img.shields.io/badge/STATUS-CONCLUÍDO-green?style=for-the-badge)

---

## 📌 Descrição do Projeto

Este projeto foi desenvolvido como parte da disciplina de **Análise de Dados** na
**Faculdade Engenheiro Salvador Arena (FESA)**. A solução aborda o problema de
**mortalidade por sífilis congênita no estado de Minas Gerais**, utilizando um
pipeline completo de Engenharia de Dados, Análise Estatística, Machine Learning e
Business Intelligence.

A sífilis congênita é uma doença de notificação compulsória e inteiramente
prevenível. Apesar disso, o Brasil ainda registra milhares de casos anuais com
desfechos fatais — muitos associados à ausência ou inadequação do diagnóstico e
tratamento durante o pré-natal. Este projeto aplica técnicas de ciência de dados
para identificar padrões populacionais e apoiar decisões de saúde pública.

> ⚠️ **Aviso:** Esta ferramenta é de **apoio epidemiológico populacional**.
> Não realiza diagnósticos clínicos individuais nem substitui avaliação médica.

---

## 👥 Equipe

| Integrante | RM | Responsabilidade |
| :--- | :--- | :--- |
| Gustavo Correia Scarabeli | 082210030 | Engenharia de Dados / Coordenação |
| Artur Rossi Junior | 082210044 | Machine Learning / Modelagem |
| Matheus Andrade de Oliveira | 082210020 | EDA / Análise Estatística |
| Gustavo Correa Pedro de Carvalho | 082210018 | BI / Dashboard / Documentação |

---

## 🗃️ Dataset

- **Fonte:** SINAN (Sistema de Informação de Agravos de Notificação) / DATASUS
- **Período:** 2010 – 2026
- **Volume:** 33.345 registros
- **Cobertura:** 853 municípios · 28 Regionais de Saúde de Minas Gerais
- **Variável-alvo:** Desfecho clínico da criança (óbito por sífilis congênita vs. nascido vivo)

---

## 🚀 Entregas e Metodologia

### M1 — Data Engineering (Pipeline ETL)

Construção de pipeline para consumo de dados do SINAN via DATASUS.

- **Arquitetura:** Star Schema com Tabelas Fato e Dimensão
- **Dimensões:** Tempo, Regional de Saúde, Diagnóstico Materno, Tratamento, Perfil Demográfico
- **Armazenamento:** Camadas `raw` e `processed` no Google Drive
- **Tecnologias:** Python, Pandas, Google Colab

### M2 — Exploratory Data Analysis (EDA)

Exploração estatística para validação de hipóteses e caracterização do dataset.

- **Análise Univariada/Multivariada:** Identificação de outliers e distribuição de variáveis
- **Desbalanceamento:** Taxa de óbito ~1,35% exigiu estratégias específicas de modelagem
- **Correlação:** Identificação das variáveis mais associadas ao desfecho adverso
- **Insight-chave:** A ausência de diagnóstico no pré-natal combinada com tratamento
  não realizado eleva a probabilidade de óbito em até 7×

### M3 — Modelagem Preditiva (Machine Learning)

Desenvolvimento e comparação de modelos de classificação para previsão do desfecho.

| Modelo | Acurácia | F1-Score | AUC-ROC | Tempo (ms) |
| :--- | :---: | :---: | :---: | :---: |
| Regressão Logística | 0.7209 | 0.0471 | **0.6958** | 724 |
| Random Forest | 0.7818 | 0.0446 | 0.6527 | 3.682 |
| Gradient Boosting | 0.9865 | 0.0000 | 0.6811 | 5.603 |
| KNN | 0.9865 | 0.0000 | 0.5658 | 223 |

**Modelo Final:** Regressão Logística — escolhida pelo maior **AUC-ROC (0.6958)**,
melhor capacidade de distinguir casos positivos em dataset desbalanceado e maior
interpretabilidade para validação clínica.

### M4 — Business Insights & GenAI

Transformação dos resultados em valor estratégico para gestores de saúde pública.

- **Dashboard Interativo (Streamlit):** Visualização multidimensional com filtros OLAP por
  tempo, regional, diagnóstico materno, tratamento e perfil demográfico. Inclui Drill-down
  hierárquico (diagnóstico → tratamento → desfecho), Heatmaps (Pivot Ano × Diagnóstico,
  Regional × Tratamento), KPIs em tempo real e Simulador de Risco Individual com Gauge
- **Agente de IA (Google AI Studio):** Prompt de sistema especializado em epidemiologia
  de sífilis congênita para o Gemini, gerando análises qualitativas e planos de ação
  acionáveis baseados nos dados do dashboard

---

## 📺 Apresentação e Demonstração

[ 🎥 **[ASSISTIR AO VÍDEO DO PITCH (2 MIN)](https://youtu.be/teO4O1Yxsbg)**
> *Resumo do problema, metodologia, demonstração do dashboard e impacto social da solução.*

> 🤖 **[ACESSAR AGENTE DE INSIGHTS — GOOGLE AI STUDIO](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%2215AI09-lKM3wcd-DiZ0sE-SGTlMGtpYYK%22%5D,%22action%22:%22open%22,%22userId%22:%22104313013169065559048%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing)**
> *Interaja com a IA especializada em epidemiologia de sífilis congênita para análise
> dos dados e geração de planos de ação em saúde pública.*

> 📊 **[ACESSAR DASHBOARD](https://datastormproject.streamlit.app/)**
> *Dashboard interativo com visualizações OLAP dos dados SINAN-MG 2010–2026.*

---

## 🛠️ Como Reproduzir

```bash
# 1. Clone o repositório
git clone https://github.com/gscarabeli/DATA_STORM_Project.git
cd DATA_STORM_Project

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o dashboard localmente
streamlit run dashboards/dashboard.py

# 4. Execute o notebook no Google Colab
# Abra notebooks/DATA_STORM_Project.ipynb via Google Colab
# Configure o caminho do Google Drive para leitura dos arquivos em /data
```

### Dependências principais

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scikit-learn>=1.3.0
```

---

## 📂 Estrutura do Repositório

```
DATA_STORM_Project/
│
├── notebooks/
│   └── DATA_STORM_Project.ipynb     # Pipeline completo: ETL → EDA → ML → BI
│
├── models/
│   └── logistic_regression_final.pkl  # Modelo serializado (produção)
│
├── dashboards/
│   └── dashboard.py                 # Dashboard Streamlit (M4)
│
├── prompts/
│   └── google_ai_studio_prompt.md   # System Prompt do Agente de Insights (M4)
│
├── requirements.txt
└── README.md
```

---

## 💡 Impacto e Relevância

A sífilis congênita é uma das principais causas evitáveis de mortalidade neonatal no
Brasil. Em Minas Gerais, os dados do SINAN revelam que a grande maioria dos desfechos
fatais está diretamente associada à **falha no diagnóstico pré-natal** e ao
**tratamento inadequado** — fatores identificados pelo modelo preditivo deste projeto.

A ferramenta desenvolvida permite que gestores de saúde pública:
- Monitorem indicadores críticos em tempo real por regional
- Identifiquem padrões populacionais de risco com navegação OLAP
- Recebam recomendações de intervenção geradas por IA especializada
- Fundamentem decisões de alocação de recursos na Atenção Básica

---

<p align="center">
  <img src="https://faculdadesalvadorarena.org.br/wp-content/uploads/2022/07/logo_fesa.png" width="180" alt="Logo FESA"><br>
  <b>Faculdade Engenheiro Salvador Arena</b><br>
  Curso de Engenharia de Computação · Maio de 2026
</p>
