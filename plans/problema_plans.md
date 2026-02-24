## Objetivo

Criar um web scraping do site **Vitrine Sebrae Startups** para coletar dados das startups (listagem paginada e página de detalhe) e gerar um arquivo estruturado para uso em análises e dashboards.

---

## Atividades

Analisar a paginação e a estrutura do site: https://vitrine.sebraestartups.com.br/?hasTag=true&page=1
Identificar os campos disponíveis na listagem
Implementar um script em Python no arquivo main.py
Criar um script colab com seu nome
Extrair os dados das startups (ex.: "type", "name", "local", "segment_pt", "maturity_pt", "siteUrl", "email", "phone", "description_pt", "imageUrl") de todas as páginas
Tratar erros básicos (retry)
Exportar os dados coletados em CSV, e o nome do arquivo CSV deve conter a data e a hora em que foram coletados.
Código deve ser documentado nas próprias funções em ligua protuguesa

---

## Definição de Pronto

- Script de scraping executando corretamente e sem necessidade de ajustes manuais.
- Arquivo `vitrine_startups_{data-hora}.csv` gerado com dados estruturados.
- Link do código gerado incluído em comentário neste card.
