# Simple Scraper — Vitrine Sebrae Startups

## Descrição do Projeto

Projeto Python para coletar dados das startups listadas em https://vitrine.sebraestartups.com.br. O repositório contém duas implementações de scraping: uma com Playwright (`main.py`) e outra com Selenium (`scraper.py`). O resultado é um CSV com informações estruturadas sobre cada startup (nome, local, segmento, estágio, site, email, telefone, descrição e imagem).

## Requisitos

- Python 3.8 ou superior
- Google Chrome / Chromium (ou instalação do navegador via Playwright)
- Dependências Python (ver seção Instalação)

## Instalação

1. Clonar o repositório:

```bash
git clone https://github.com/rubenspinto/simple-scraper.git
cd simple-scraper
```

2. Criar e ativar um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate
```

3. Instalar dependências (exemplo mínimo):

```bash
pip install playwright beautifulsoup4 pandas selenium
playwright install chromium
```

(Se preferir, crie um `requirements.txt` com as dependências e rode `pip install -r requirements.txt`.)

## Uso

O script por padrão está configurado para executar um número pequeno de páginas para testes; ajuste o parâmetro `max_paginas` dentro do arquivo ou modifique a chamada em `if __name__ == '__main__'` para coletar todas as páginas necessárias.

- Executar a versão Selenium:

```bash
python scraper.py
```

Observações:
- Ambos os scripts salvam CSVs com nome contendo timestamp. `main.py` gera um CSV com timestamp e `scraper.py` gera `startups_completo.csv`.
- Se usar Selenium, garanta que o ChromeDriver compatível esteja instalado/na `PATH`, ou configure `webdriver.Chrome()` adequadamente.

## Estrutura de Arquivos

- `scraper.py` — Scraper Selenium: alternativa que intercepta clipboard para capturar emails/telefones, ou seja, extrai dados e salva Ccomo um arquivo CSV.
- `startups_completo.csv` — Exemplo/resultado gerado pelo scraper (dados coletados).
- `venv/` — Ambiente virtual (não versionar o ambiente em repositório público).

## Contribuindo

- Abra uma issue para discutir mudanças ou melhorias.
- Faça um fork e envie pull requests claros e pequenos.
- Adicione testes quando alterar lógica de parsing ou extração.
- Atualize `requirements.txt` se adicionar/alterar dependências.

## Boas práticas ao rodar o scraper

- Respeite o `robots.txt` e os termos do site alvo.
- Use delays entre requisições (os scripts já adicionam pequenas pausas).
- Evite alta taxa de requisições para não sobrecarregar o site.

## Licença

Licença: MIT

## Contato

- Mantentor: [Rubens] — email: [rubenssi825@gmail.com.com]
- Para dúvidas ou melhorias: abra uma issue neste repositório.
