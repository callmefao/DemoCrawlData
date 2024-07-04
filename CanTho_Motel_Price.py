from bs4 import BeautifulSoup
import requests
import json
from Split_From_Description import get_area, get_price, get_contact
import re

def get_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', class_='row large-columns-1 medium-columns- small-columns-1 row-xsmall')
    rows = table.find_all('div', class_="col-inner")
    links = set()
    for row in rows:
        tag_a = row.find('a')
        curr_link = tag_a['href']
        links.add(curr_link)
    return links


def get_title(rows):
    try:
        title = rows.find('h2').get_text(strip=True)
    except:
        try:
            title = rows.find('strong').get_text(strip=True)
        except:
            title = "No Info"
    return title


def get_tag(rows):
    tags = rows.find_all('div', dir="auto")
    if not tags:
        tags = rows.find_all(['p', 'ul'])
    if not tags:
        tags = rows.find_all('div')
    return tags


def extract_motel(links):
    Motel_info_list = []

    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find('div', class_="entry-content single-page")

        title = get_title(rows)
        tags = get_tag(rows)

        description = ""
        for div in tags:
            description += (div.get_text(strip=True) + "\n")
            Motel_info = {
                'link': link,
                'title': title,
                'description': description,
                'price': get_price(description + title),
                'area': get_area(description),
                'contact': get_contact(description)
            }
        Motel_info_list.append(Motel_info)

    return Motel_info_list


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    url = "https://nhatrocantho.top/"

    urls = get_link(url)
    Motel_info_list = extract_motel(urls)
    save_to_json(Motel_info_list, 'CanTho_Motel.json')
