"""
Popula o histórico com uma execução "de ontem" fictícia (alguns preços
levemente diferentes dos atuais), só pra demonstrar a detecção de
mudança de preço sem precisar esperar dias o site real mudar de fato.

Rode isso UMA VEZ antes da primeira execução de monitor.py.
Uso: python seed_demo_history.py
"""
import random
import sqlite3
from datetime import datetime, timedelta

from monitor import DB, init_db
from scraper import scrape_catalog

random.seed(7)


def main():
    conn = sqlite3.connect(DB)
    init_db(conn)

    items = scrape_catalog(max_pages=3)
    ontem = (datetime.now() - timedelta(days=1)).isoformat(timespec="seconds")

    for item in items:
        fator = random.choice([1.0, 1.0, 1.0, 0.9, 1.15])
        preco_simulado = round(item["price"] * fator, 2)
        conn.execute(
            "INSERT INTO price_history VALUES (?, ?, ?, ?)",
            (item["title"], preco_simulado, item["availability"], ontem),
        )

    conn.commit()
    conn.close()
    print(f"Histórico simulado de {len(items)} produtos inserido (data: {ontem}).")
    print("Agora rode: python monitor.py")


if __name__ == "__main__":
    main()
