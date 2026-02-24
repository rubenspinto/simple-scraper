# Plano de Ação Simplificado: Webscraper Sebrae Startups

Este plano visa a criação de um script Python para coletar dados das startups listadas na Vitrine Sebrae.

## 1. Análise e Estratégia

- **Verificação da Fonte de Dados:** Identificar se o site carrega os dados via HTML estático ou requisições de API (JSON). A estratégia de extração dependerá disso (BeautifulSoup vs Requests direto na API).
- **Mapeamento de Paginação:** Entender o parâmetro `page=X` na URL ou na API para iterar por todas as startups.

## 2. Desenvolvimento do Script

- **Estrutura Básica:** Utilizar `requests` e `BeautifulSoup` (ou manipulação de JSON se for API).
- **Campos a Extrair:**
  - `type`
  - `name`
  - `local`
  - `segment_pt`
  - `maturity_pt`
  - `siteUrl`
  - `email`
  - `phone`
  - `description_pt`
  - `imageUrl`
- **Funcionalidades Críticas:**
  - **Paginação Automática:** Loop para percorrer todas as páginas disponíveis.
  - **Tratamento de Erros:** Implementar `try/except` e tentativas de re-conexão (retry) caso a requisição falhe.
  - **Exportação:** Gerar arquivo CSV com nome dinâmico: `vitrine_startups_YYYY-MM-DD_HH-MM.csv`.

## 3. Validação

- **Teste de Execução:** Rodar o script e verificar se o CSV é gerado corretamente.
- **Conferência de Dados:** Validar se os campos estão preenchidos e se o número de registros condiz com o total do site.
