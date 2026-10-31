import json
import urllib.request
from datetime import datetime, timezone

PRODUCT_ID = 1605620355
URL = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={PRODUCT_ID}"
request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
with urllib.request.urlopen(request, timeout=25) as response:
    payload = json.load(response)
products = payload.get("data", {}).get("products", [])
if not products or int(products[0].get("id", 0)) != PRODUCT_ID:
    raise RuntimeError("Wildberries API did not return the requested product")
product = products[0]
price_kopecks = product.get("salePriceU")
if not isinstance(price_kopecks, (int, float)) or price_kopecks <= 0:
    prices = [size.get("price", {}).get("product") for size in product.get("sizes", [])]
    prices = [p for p in prices if isinstance(p, (int, float)) and p > 0]
    if not prices:
        raise RuntimeError("No current price in Wildberries response")
    price_kopecks = min(prices)
result = {
    "product_id": PRODUCT_ID,
    "price": round(price_kopecks / 100),
    "currency": "RUB",
    "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "source": "Wildberries product card API"
}
with open("price.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)
    file.write("\n")
print(json.dumps(result, ensure_ascii=False))
