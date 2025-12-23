import csv
import re
from typing import List, Dict, Optional


def _find_key(header: List[str], candidates: List[str]) -> Optional[str]:
    low = [h.lower() for h in header]
    for c in candidates:
        if c.lower() in low:
            return header[low.index(c.lower())]
    # try substring match
    for h in header:
        for c in candidates:
            if c.lower() in h.lower():
                return h
    return None


def _parse_number(s: str) -> Optional[float]:
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return None
    # Remove currency symbols and commas
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return float(s)
    except ValueError:
        return None


def read_products(path: str = "Products.csv") -> List[Dict[str, str]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


def print_rows(rows: List[Dict[str, str]]):
    if not rows:
        print("No rows to display.")
        return
    header = list(rows[0].keys())
    name_key = _find_key(header, ["productname", "product", "name"]) or header[0]
    category_key = _find_key(header, ["category", "cat"]) or header[0]
    price_key = _find_key(header, ["price", "cost", "amount"]) or header[0]
    qty_key = _find_key(header, ["quantity", "qty", "stock"]) or header[0]

    for i, r in enumerate(rows, 1):
        name = r.get(name_key, "")
        cat = r.get(category_key, "")
        price = r.get(price_key, "")
        qty = r.get(qty_key, "")
        print(f"{i}. Product: {name} | Category: {cat} | Price: {price} | Quantity: {qty}")


def total_rows(rows: List[Dict[str, str]]) -> int:
    return len(rows)


def count_price_above(rows: List[Dict[str, str]], threshold: float = 500.0) -> int:
    header = list(rows[0].keys()) if rows else []
    price_key = _find_key(header, ["price", "cost", "amount"]) if header else None
    cnt = 0
    if not price_key:
        return 0
    for r in rows:
        p = _parse_number(r.get(price_key, ""))
        if p is not None and p > threshold:
            cnt += 1
    return cnt


def average_price(rows: List[Dict[str, str]]) -> Optional[float]:
    header = list(rows[0].keys()) if rows else []
    price_key = _find_key(header, ["price", "cost", "amount"]) if header else None
    if not price_key:
        return None
    vals = [v for v in (_parse_number(r.get(price_key, "")) for r in rows) if v is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def products_in_category(rows: List[Dict[str, str]], category: str) -> List[Dict[str, str]]:
    if not rows:
        return []
    header = list(rows[0].keys())
    category_key = _find_key(header, ["category", "cat"]) or header[0]
    return [r for r in rows if (r.get(category_key, "") or "").strip().lower() == category.strip().lower()]


def total_quantity(rows: List[Dict[str, str]]) -> int:
    if not rows:
        return 0
    header = list(rows[0].keys())
    qty_key = _find_key(header, ["quantity", "qty", "stock"]) or header[0]
    total = 0
    for r in rows:
        val = r.get(qty_key, "")
        try:
            total += int(float(val))
        except Exception:
            num = _parse_number(val)
            if num is not None:
                total += int(num)
            else:
                continue
    return total


def main():
    path = input("Enter CSV file path [Products.csv]: ") or "Products.csv"
    try:
        rows = read_products(path)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    print("\n--- Rows (clean format) ---")
    print_rows(rows)

    total = total_rows(rows)
    print(f"\nTotal number of rows: {total}")

    above_500 = count_price_above(rows, 500.0)
    print(f"Total number of products priced above 500: {above_500}")

    avg = average_price(rows)
    if avg is None:
        print("Average price: N/A")
    else:
        print(f"Average price of all products: {avg:.2f}")

    cat = input("\nEnter a category to list products (case-insensitive): ")
    if cat.strip():
        matched = products_in_category(rows, cat)
        if matched:
            print(f"\nProducts in category '{cat}':")
            for r in matched:
                print("-", r)
        else:
            print(f"No products found in category '{cat}'.")

    total_qty = total_quantity(rows)
    print(f"\nTotal quantity of all items in stock: {total_qty}")


if __name__ == "__main__":
    main()
