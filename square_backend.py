import os
from square.client import Client
from dotenv import load_dotenv

# 載入 .env 檔中的環境變數
load_dotenv()

SQUARE_APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID")
SQUARE_ACCESS_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")

# 建立 Square 客戶端連線（sandbox 環境）
client = Client(
    access_token=SQUARE_ACCESS_TOKEN,
    environment="sandbox"
)

def fetch_catalog_items():
    """
    使用 Catalog API 取得菜單 ITEM 資料
    """
    catalog_api = client.catalog
    result = catalog_api.list_catalog(types="ITEM", limit=50)
    if result.is_success():
        # 從回應中取得 objects，通常其中含有菜單或其他商品資料
        objects = result.body.get("objects", [])
        return objects
    else:
        raise Exception(f"Error fetching catalog: {result.errors}")

if __name__ == "__main__":
    try:
        items = fetch_catalog_items()
        print("取得的菜單項目：")
        for item in items:
            item_data = item.get("item_data", {})
            item_name = item_data.get("name", "未命名項目")
            print(f"- {item.get('id')}: {item_name}")
    except Exception as e:
        print("取得菜單項目失敗：", e) 