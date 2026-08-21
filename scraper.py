"""
Scraper de catálogo de produtos (título, preço, disponibilidade).

Roda aqui contra books.toscrape.com — um site público mantido
especificamente pra prática de scraping — mas a estrutura serve pra
monitorar o catálogo de qualquer concorrente real: basta trocar a URL
base e os seletores CSS pelos do site alvo.
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"


def parse_price(text: str) -> float:
    return float(text.replace("£", "").strip())


def scrape_page(page: int) -> list[dict]:
    resp = requests.get(BASE_URL.format(page), timeout=10)
    resp.raise_for_status()
    # o servidor não declara charset no header, então requests assume
    # ISO-8859-1 por padrão e corrompe o símbolo "£" — passar os bytes
    # crus deixa o BeautifulSoup detectar o encoding real (UTF-8)
    soup = BeautifulSoup(resp.content, "html.parser")

    items = []
    for product in soup.select("article.product_pod"):
        items.append({
            "title": product.h3.a["title"],
            "price": parse_price(product.select_one(".price_color").text),
            "availability": product.select_one(".availability").text.strip(),
        })
    return items


def scrape_catalog(max_pages: int = 3) -> list[dict]:
    all_items = []
    for page in range(1, max_pages + 1):
        all_items.extend(scrape_page(page))
    return all_items


if __name__ == "__main__":
    produtos = scrape_catalog(max_pages=1)
    print(f"{len(produtos)} produtos encontrados na página 1:")
    for p in produtos[:5]:
        print(f"  {p['title'][:40]:<40} £{p['price']}  ({p['availability']})")
