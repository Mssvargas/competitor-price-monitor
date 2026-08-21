"""
Monitor de preços: roda o scraper, guarda histórico em SQLite e gera um
relatório apontando o que mudou desde a última execução (produto novo,
preço subiu, preço caiu).

Pensado pra rodar agendado (cron / Agendador de Tarefas do Windows) uma
vez por dia, comparando sempre contra a execução anterior.

Uso: python monitor.py
"""
import sqlite3
from datetime import datetime

import pandas as pd

from scraper import scrape_catalog

DB = "price_history.db"
RELATORIO = "alertas_preco.xlsx"


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            title TEXT, price REAL, availability TEXT, checked_at TEXT
        )
    """)


def last_snapshot(conn) -> dict:
    rows = conn.execute("""
        SELECT title, price FROM price_history
        WHERE checked_at = (SELECT MAX(checked_at) FROM price_history)
    """).fetchall()
    return dict(rows)


def main():
    conn = sqlite3.connect(DB)
    init_db(conn)

    anterior = last_snapshot(conn)
    items = scrape_catalog(max_pages=3)
    agora = datetime.now().isoformat(timespec="seconds")

    mudancas = []
    for item in items:
        preco_antigo = anterior.get(item["title"])
        if preco_antigo is None:
            mudancas.append({"produto": item["title"], "status": "novo", "de": None, "para": item["price"]})
        elif preco_antigo != item["price"]:
            status = "subiu" if item["price"] > preco_antigo else "caiu"
            mudancas.append({"produto": item["title"], "status": status, "de": preco_antigo, "para": item["price"]})

        conn.execute(
            "INSERT INTO price_history VALUES (?, ?, ?, ?)",
            (item["title"], item["price"], item["availability"], agora),
        )

    conn.commit()
    conn.close()

    if mudancas:
        pd.DataFrame(mudancas).to_excel(RELATORIO, index=False)
        print(f"{len(mudancas)} mudança(s) detectada(s) -> {RELATORIO}")
    else:
        print("Nenhuma mudança desde a última execução.")

    print(f"{len(items)} produtos verificados em {agora}")


if __name__ == "__main__":
    main()
