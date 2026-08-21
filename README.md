# Monitor de Preços de Concorrentes

Faz scraping de um catálogo de produtos periodicamente, guarda o
histórico e gera um relatório apontando o que mudou desde a última
checagem: produto novo, preço subiu ou preço caiu.

## O problema que isso resolve

"Monitorar preço de concorrente", "avisar quando o preço de X mudar" e
"extrair dados de um site" estão entre os pedidos mais comuns de
automação/scraping em plataformas freelance. Qualquer loja quer saber
quando um concorrente baixa o preço de um produto que ela também vende.

## O que o projeto entrega

1. **`scraper.py`** — faz scraping de um catálogo de produtos (título,
   preço, disponibilidade). Rodando aqui contra
   [books.toscrape.com](https://books.toscrape.com), um site público
   feito justamente pra prática de scraping — a estrutura serve pra
   monitorar o catálogo de qualquer concorrente real, trocando a URL e
   os seletores CSS.
2. **`monitor.py`** — roda o scraper, salva cada checagem no SQLite
   (`price_history.db`) e compara com a checagem anterior, gerando
   `alertas_preco.xlsx` com os produtos que mudaram de preço.
3. **`seed_demo_history.py`** — só pra demonstração: popula um histórico
   "de ontem" com alguns preços levemente diferentes, pra já dar pra ver
   o monitor detectando mudanças na primeira vez que você roda, sem
   precisar esperar o site real mudar de preço.

## Como rodar

```bash
pip install -r requirements.txt
python seed_demo_history.py   # só na primeira vez, pra ter histórico de comparação
python monitor.py             # roda a checagem real e gera o relatório
```

Rodando `python monitor.py` de novo sem nada mudar no site real, o
relatório correto é "nenhuma mudança".

## Adaptar para um cliente real

Troca `BASE_URL` e os seletores CSS em `scraper.py` pelo site do
concorrente real do cliente, e agenda `monitor.py` pra rodar 1x por dia
(cron no Linux, Agendador de Tarefas no Windows).

## Stack

Python, requests, BeautifulSoup, SQLite, pandas/openpyxl.

## Como usar isso no perfil freelancer

- Print do `alertas_preco.xlsx` mostrando produtos com preço subindo/caindo.
- Descrição sugerida: *"Automatizo o monitoramento de preços de
  concorrentes: scraping diário + alerta de qualquer mudança de preço."*
