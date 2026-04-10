# DATA STORM Project - Análise de Sífilis Congênita em Minas Gerais

## Resumo do Problema

Este projeto visa prever o desfecho clínico da criança (óbito por sífilis congênita vs. nascido vivo) com base em dados de notificações de sífilis congênita no estado de Minas Gerais, extraídos do SINAN. O período analisado vai de 2010 a 2026, com 33.345 registros distribuídos em 853 municípios e 28 regionais de saúde. Os fatores considerados incluem momento do diagnóstico materno, adequação do tratamento e perfil demográfico.

## Tabela Comparativa

Resultados finais dos modelos testados:

| Modelo              | Acurácia | F1-Score | AUC-ROC | Tempo (ms) |
|---------------------|----------|----------|---------|------------|
| Regressão Logística | 0.7209   | 0.0471   | 0.6958  | 724.0      |
| Random Forest       | 0.7818   | 0.0446   | 0.6527  | 3682.0     |
| Gradient Boosting   | 0.9865   | 0.0000   | 0.6811  | 5603.0     |
| KNN                 | 0.9865   | 0.0000   | 0.5658  | 223.0      |

## Modelo Final

O modelo escolhido para produção é a **Regressão Logística**, devido ao maior AUC-ROC (0.6958). Este modelo oferece o melhor equilíbrio para distinguir entre casos positivos (óbito) e negativos (nascido vivo) em um dataset desbalanceado, além de maior interpretabilidade para validação clínica.

## Instruções de Reprodução

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute o notebook `notebooks/DATA_STORM_Project.ipynb` em um ambiente Python (recomendado: Jupyter Notebook ou Google Colab).