import re
from Formatting_Data import process_price, process_area, process_contact


def get_price(description):
    pattern = r'(\d+\s?tr\s?\d+)|(\d+\s?triệu\s?\d+)|(\b\d+[.,]?\d{0,2}\s?triệu\b)|(\b\d+[.,]?\d?\s?tr\b)|(\d+[.\s]\d+[.,]000)'
    price_matches = re.findall(pattern, description.lower())
    prices = set()
    for match in price_matches:
        for item in match:
            if item:
                prices.add(f"{process_price(pattern, item)} VND")
                break
    return ' - '.join(prices) if prices else "No info"


def get_area(description):  # Need to fix
    pattern = r'(\d+m2)|(\d+\s?m²)|([\d.,]+\s?x\s?[\d.,]+)|(\d+m\s?x\s?\d+m)'
    area_matches = re.findall(pattern, description.lower())
    areas = set()
    for match in area_matches:
        for item in match:
            if item:
                areas.add(f"{process_area(pattern, item)} m²")
                break
    if areas:
        return ' | '.join(areas)
    else:
        return "No info"


def get_contact(description):
    pattern = r'(\d{10,11})|(\d{2}[.\s]\d{4}[.\s]\d{4})|(\d{4}[.\s]\d{2}[.\s]\d{2}[.\s]\d{2})|(\d{4}[.\s]\d{3}[.\s]\d{3})'
    contact_matches = re.findall(pattern, description)
    contacts = set()
    for match in contact_matches:
        for item in match:
            if item:
                contacts.add(process_contact(pattern, item))
                break
    if contacts:
        return ' | '.join(contacts)
    else:
        return "No info"