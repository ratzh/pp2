import re


def clean_price(value):
    return float(value.replace(" ", "").replace(",", "."))


def parse_receipt(text):
    data = {}
    data["company"] = re.search(r"Филиал (.+)", text)
    data["BIN"] = re.search(r"БИН (\d+)", text)
    data["receipt_number"] = re.search(r"Чек №(\d+)", text)
    data["total"] = re.search(r"ИТОГО:\s*([\d\s]+,\d{2})", text)
    data["datetime"] = re.search(
        r"Время:\s*(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})", text
    )

    for key in data:
        if data[key]:
            data[key] = data[key].group(1)

    if data["total"]:
        data["total"] = clean_price(data["total"])

    items = re.findall(
        r"\d+\.\n(.+?)\n([\d,]+) x ([\d\s]+,\d{2})\n([\d\s]+,\d{2})",
        text,
        re.MULTILINE,
    )

    parsed_items = []
    for name, qty, price, total in items:
        parsed_items.append({
            "name": name.strip(),
            "quantity": float(qty.replace(",", ".")),
            "unit_price": clean_price(price),
            "total_price": clean_price(total),
        })

    data["items"] = parsed_items

    return data


def print_data(data):
    print("\n--- RECEIPT ---")
    print("Company:", data.get("company"))
    print("BIN:", data.get("BIN"))
    print("Receipt #:", data.get("receipt_number"))
    print("Date & Time:", data.get("datetime"))
    print("Total:", data.get("total"))

    print("\nItems:")
    for item in data["items"]:
        print(f"{item['name']}")
        print(f"  {item['quantity']} x {item['unit_price']} = {item['total_price']}")


if __name__ == "__main__":
    with open("raw.txt", encoding="utf-8") as f:
        text = f.read()

    receipt = parse_receipt(text)
    print_data(receipt)