import re


def process_price(pattern, price_str):
    price_matches = re.findall(pattern, price_str)
    for match in price_matches:
        for index, price in enumerate(match):
            if price:
                return str(process_price_group(index, price))
    return "No Info"


def process_area(pattern, area_str):
    arae_matches = re.findall(pattern, area_str)
    for match in arae_matches:
        for index, area in enumerate(match):
            if area:
                return str(process_area_group(index, area))
    return "No Info"


def process_contact(pattern, contact_str):
    contact_matches = re.findall(pattern, contact_str)
    for match in contact_matches:
        for index, contact in enumerate(match):
            if contact:
                return str(contact.replace('.', '').replace(' ', ''))
    return "No Info"


def process_price_group(index, price):
    if index == 1 or index == 0:
        return price_type_1(price)
    elif index == 2 or index == 3:
        return price_type_2(price)
    elif index == 4:
        return str(float(price.replace('.', '')))
    else:
        raise ValueError(f"Unsupported group index: {index}")


def process_area_group(index, area):
    area = area.replace(' ', '')
    if index == 0 or index == 1:
        return float(area[:area.index('m')])
    elif index == 2 or index == 3:
        area = area.replace('m', '').replace(',', '.')
        x_location = area.index('x')
        return float(area[:x_location]) * float(area[x_location + 1:])
    else:
        raise ValueError(f"Unsupported group index: {index}")


def price_type_2(price):
    price = price.replace(',', '.').replace(' ', '').replace('triệu', '').replace('tr', '')
    if '.' in price:
        price_int = int(price[:price.index('.')]) * 1e6 + int(price[price.index('.') + 1:]) * 1e5
    else:
        price_int = int(price) * 1e6
    return price_int


def price_type_1(price):
    price = price.replace(' ', '').replace('triệu', 'tr')
    Multiply_by = [1e6, 1e5, 1e4, 1e3, 1e2, 1e1, 1e0]
    After_Million_Part = price[price.index('r') + 1:]
    After_Million_Part = int(After_Million_Part) * Multiply_by[len(After_Million_Part)]
    price_int = int(price[:price.index('t')]) * 1e6 + After_Million_Part
    return price_int
