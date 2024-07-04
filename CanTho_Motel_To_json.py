import requests
from bs4 import BeautifulSoup
import json

from Split_From_Description import get_area, get_price, get_contact


def get_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    total_col = soup.find('div', class_='row large-columns-1 medium-columns- small-columns-1 row-xsmall')
    col_inner = total_col.find_all('div', class_="col-inner")
    links = set()
    for row in col_inner:
        tag_a = row.find('a')
        curr_link = tag_a['href']
        links.add(curr_link)
    return links


def get_title(col_inner):
    try:
        title = col_inner.find('h2').get_text(strip=True)
    except:
        try:
            title = col_inner.find('strong').get_text(strip=True)
        except:
            title = "No Info"
    return title


def get_tag(entry_content):
    tag = entry_content.find_all('div', dir="auto")
    if not tag:
        tag = entry_content.find_all(['p', 'ul'])
    if not tag:
        tag = entry_content.find_all('div')
    return tag


def extract_motel(links):
    Motel_info_list = []

    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        entry_content = soup.find('div', class_="entry-content single-page")

        title = get_title(entry_content)
        tags = get_tag(entry_content)

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
