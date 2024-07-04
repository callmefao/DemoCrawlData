from bs4 import BeautifulSoup
import requests
import json
from Split_From_Description import get_area, get_price, get_contact
import pandas as pd


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
            Motel_info = [
                link,  # Link
                title,  # Title
                description,  # Description
                get_price(description + title),  # Price
                get_area(description),  # Area
                get_contact(description)  # Contact
            ]
        Motel_info_list.append(Motel_info)

    return Motel_info_list


def save_to_exel(data, filename):
    df = pd.DataFrame(data, columns=['link', 'title', 'description', 'price', 'area', 'contact'])
    df.to_excel(filename)


if __name__ == "__main__":
    url = "https://nhatrocantho.top/"

    urls = get_link(url)
    Motel_info_list = extract_motel(urls)
    save_to_exel(Motel_info_list, 'CanTho_Motel.xlsx')