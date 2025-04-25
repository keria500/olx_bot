from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from urllib.parse import urljoin
import urllib.parse


def parse_olx_card(card, base_url):
    # Гибкий способ найти заголовок
    title_tag = card.find(['h3', 'h4', 'h5', 'h6'])
    title = title_tag.text.strip() if title_tag else 'Без заголовка'

    # Ссылка на объявление
    link_tag = card.find('a', href=True)
    link = base_url + link_tag['href'] if link_tag else 'Нет ссылки'

    # Гибкий способ найти цену
    price_tag = card.find('p', {'data-testid': 'ad-price'}) or card.find('span', string=lambda s: 'лв' in s if s else False)
    price = price_tag.text.strip() if price_tag else 'Цена не указана'

    return {
        'title': title,
        'link': link,
        'price': price
    }


def search_olx(query):
    base_url = "https://www.olx.bg"
    url = f"{base_url}/ads/q-{query}/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    results = []
    cards = soup.find_all("div", {"data-cy": "l-card"})

    for card in cards:
        data = parse_olx_card(card, base_url)
        results.append(data)

    return results


if __name__ == "__main__":
    results = search_olx("Папагал")
    for ad in results:
        print(f"{ad['title']} — {ad['link']}")
